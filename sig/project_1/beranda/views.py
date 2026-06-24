from django.shortcuts import render
from django.http import HttpResponse
from .models import Province,NamaData, Datprof

# Create your views here.
def index(request):
    return HttpResponse("Selamat Datang di Halaman Beranda")

def welcome(request):
    return render(request, 'welcome.html')

def about(request):
    return render(request, 'about.html')


def peta_provinsi(request):
    data_namadata = NamaData.objects.all()
    selected_nama_data = request.GET.get('nama_data', '')

    # Ambil semua provinsi
    data_provinsi = Province.objects.all()

    # Jika ada nama data yang dipilih, ambil datprof-nya
    datprof_map = {}
    if selected_nama_data:
        datprofs = Datprof.objects.filter(nama_id=selected_nama_data).select_related('province')
        for d in datprofs:
            datprof_map[d.province_id] = {
                'tahun': d.tahun,
                'jumlah': d.jumlah,
            }

    # Gabungkan data provinsi dengan datprof
    provinsi_dengan_data = []
    for p in data_provinsi:
        item = {
            'id': p.id,
            'name': p.name,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'tahun': datprof_map.get(p.id, {}).get('tahun', '-'),
            'jumlah': datprof_map.get(p.id, {}).get('jumlah', '-'),
        }
        provinsi_dengan_data.append(item)

    return render(request, 'peta_provinsi.html', {
        'data_provinsi': provinsi_dengan_data,
        'data_namadata': data_namadata,
        'selected_nama_data': selected_nama_data,
    })


def kepadatan_penduduk(request):
    # Ambil semua data kepadatan penduduk dari database
    # data_kepadatan = Datprof.objects.all()
    provinsi = Province.objects.all()
    provinsi_terpilih = request.GET.get('provinsi_terpilih')
    if provinsi_terpilih:
        provinsi_terpilih = int(provinsi_terpilih)
        #data_kepadatan = Datprof.objects.filter(provinsi__id=provinsi_terpilih)
        pass
    
    return render(request, 'kepadatan_penduduk.html', {
        'provinsi': provinsi,
        'provinsi_terpilih': provinsi_terpilih,
    })