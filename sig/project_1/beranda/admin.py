from django.contrib import admin
from .models import Province, Regency, District, NamaData, Datprof


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'alt_name', 'latitude', 'longitude')
    search_fields = ('name', 'alt_name')
    list_filter = ('name', 'latitude')


@admin.register(Regency)
class RegencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "province", "latitude", "longitude")
    search_fields = ("name",)
    list_filter = ("province",)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alt_name", "regency", "latitude", "longitude")
    search_fields = ("name", "alt_name")
    list_filter = ("regency__province", "regency")


@admin.register(NamaData)
class NamaDataAdmin(admin.ModelAdmin):
    # Menampilkan ID dan isi field name di halaman daftar
    list_display = ('id', 'name')
    
    # Fitur pencarian berdasarkan nama data/kategori
    search_fields = ('name',)


@admin.register(Datprof)
class DatprofAdmin(admin.ModelAdmin):
    # Menampilkan kolom-kolom dari model Datprof
    list_display = ('id', 'province', 'nama', 'tahun', 'jumlah')
    
    # Fitur pencarian berdasarkan nama provinsi (dari relasi), nama data (dari relasi), dan tahun
    search_fields = ('province__name', 'nama__name', 'tahun')
    
    # Fitur filter di panel kanan berdasarkan tahun, kategori data, dan provinsi
    list_filter = ('tahun', 'nama', 'province')
    
    # Mengurutkan data berdasarkan tahun terbaru
    ordering = ('-tahun', 'province')