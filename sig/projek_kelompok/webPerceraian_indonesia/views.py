from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Provinsi, DataPerceraian   # relative import


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