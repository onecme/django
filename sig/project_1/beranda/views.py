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
    data_provinsi = Province.objects.all()
    data_namadata = NamaData.objects.all()
    selected_nama_data = request.GET.get('nama_data', '')
    return render(request, 'peta_provinsi.html', {
        'data_provinsi': data_provinsi,
        'data_namadata': data_namadata,
        'selected_nama_data': selected_nama_data,
    })