from django.contrib import admin
from .models import Provinsi, DataPerceraian


@admin.register(Provinsi)
class ProvinsiAdmin(admin.ModelAdmin):
    list_display = ['id', 'kode_prov', 'nama']
    search_fields = ['nama', 'kode_prov']
    ordering = ['nama']


@admin.register(DataPerceraian)
class DataPerceraianAdmin(admin.ModelAdmin):
    list_display = [
        'provinsi',
        'tahun',
        'jumlah_perceraian',
        'faktor_perselisihan',
        'faktor_ekonomi',
    ]
    search_fields = ['provinsi__nama']
    list_filter = ['tahun']
    ordering = ['provinsi__nama']