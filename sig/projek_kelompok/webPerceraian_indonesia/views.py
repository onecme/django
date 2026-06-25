from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Provinsi, DataPerceraian   # relative import
import json
from django.conf import settings
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from groq import Groq


def landing_page(request):
    return render(request, 'landing.html')


def peta_jumlah(request):
    return render(request, 'peta.html', {
        'judul': 'Jumlah Perceraian per Provinsi (2023)',
        'kolom': 'jumlah_perceraian',
        'label': 'Jumlah Perceraian',
        'api_url': '/api/geojson/jumlah/',
        'nav_aktif': 'jumlah',
    })


def peta_perselisihan(request):
    return render(request, 'peta.html', {
        'judul': 'Perceraian Faktor Perselisihan per Provinsi (2023)',
        'kolom': 'faktor_perselisihan',
        'label': 'Faktor Perselisihan',
        'api_url': '/api/geojson/perselisihan/',
        'nav_aktif': 'perselisihan',
    })


def peta_ekonomi(request):
    return render(request, 'peta.html', {
        'judul': 'Perceraian Faktor Ekonomi per Provinsi (2023)',
        'kolom': 'faktor_ekonomi',
        'label': 'Faktor Ekonomi',
        'api_url': '/api/geojson/ekonomi/',
        'nav_aktif': 'ekonomi',
    })


@require_GET
def api_geojson_jumlah(request):
    return _build_geojson_response("jumlah_perceraian")

@require_GET
def api_geojson_perselisihan(request):
    return _build_geojson_response("faktor_perselisihan")

@require_GET
def api_geojson_ekonomi(request):
    return _build_geojson_response("faktor_ekonomi")


def _build_geojson_response(kolom):
    provinsi_list = Provinsi.objects.select_related("data_perceraian").all()
    features = []
    for prov in provinsi_list:
        try:
            dp = prov.data_perceraian
        except DataPerceraian.DoesNotExist:
            continue
        features.append({
            "type": "Feature",
            "properties": {
                "nama": prov.nama,
                "kode": prov.kode_prov,
                "nilai": getattr(dp, kolom, 0),
                "jumlah_perceraian": dp.jumlah_perceraian,
                "faktor_perselisihan": dp.faktor_perselisihan,
                "faktor_ekonomi": dp.faktor_ekonomi,
            },
            "geometry": prov.geometry,
        })
    return JsonResponse({"type": "FeatureCollection", "features": features})



# Menambah fitur Analisis LLM
@csrf_exempt
@require_POST
def api_analisis(request):
    """
    Menerima data perceraian dari frontend,
    mengirim ke Groq, dan streaming hasilnya balik ke client.
    """
    try:
        body = json.loads(request.body)
        mode = body.get('mode', 'nasional')  # 'provinsi' atau 'nasional'
        data = body.get('data', {})
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Request tidak valid'}, status=400)

    client = Groq(api_key=settings.GROQ_API_KEY)

    if mode == 'provinsi':
        nama     = data.get('nama', '-')
        jumlah   = data.get('jumlah_perceraian', 0)
        selisih  = data.get('faktor_perselisihan', 0)
        ekonomi  = data.get('faktor_ekonomi', 0)

        prompt = f"""Kamu adalah analis sosial kependudukan Indonesia yang berpengalaman.

Berikut data perceraian Provinsi {nama} tahun 2023 dari BPS:
- Total perceraian       : {jumlah:,} kasus
- Faktor perselisihan    : {selisih:,} kasus ({round(selisih/jumlah*100, 1) if jumlah else 0}% dari total)
- Faktor ekonomi         : {ekonomi:,} kasus ({round(ekonomi/jumlah*100, 1) if jumlah else 0}% dari total)

Berikan analisis singkat (3-4 paragraf) dalam Bahasa Indonesia yang mencakup:
1. Gambaran umum kondisi perceraian di provinsi ini
2. Interpretasi dominasi faktor perselisihan vs ekonomi
3. Kemungkinan faktor sosial-budaya yang mempengaruhi
4. Rekomendasi kebijakan yang relevan

Gunakan bahasa yang informatif namun mudah dipahami masyarakat umum."""

    else:  # nasional
        provinsi_list = data.get('provinsi_list', [])
        total_nasional = sum(p.get('nilai', 0) for p in provinsi_list)
        top3 = provinsi_list[:3] if len(provinsi_list) >= 3 else provinsi_list
        top3_str = ', '.join([f"{p['nama']} ({p['nilai']:,})" for p in top3])

        prompt = f"""Kamu adalah analis sosial kependudukan Indonesia yang berpengalaman.

Berikut ringkasan data perceraian Indonesia tahun 2023 dari BPS:
- Total kasus seluruh Indonesia : {total_nasional:,} kasus
- Provinsi tertinggi            : {top3_str}
- Total provinsi yang didata    : {len(provinsi_list)} provinsi

Berikan analisis nasional (3-4 paragraf) dalam Bahasa Indonesia yang mencakup:
1. Gambaran umum tingkat perceraian di Indonesia tahun 2023
2. Pola spasial — mengapa Pulau Jawa mendominasi
3. Implikasi sosial dan ekonomi dari angka perceraian ini
4. Rekomendasi kebijakan nasional yang relevan

Gunakan bahasa yang informatif namun mudah dipahami masyarakat umum."""

    def stream_generator():
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=800,
            temperature=0.7,
        )
        for chunk in completion:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    return StreamingHttpResponse(
        stream_generator(),
        content_type='text/plain; charset=utf-8'
    )