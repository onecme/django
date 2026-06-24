from django.contrib import admin
from django.urls import path
from . import views   # relative import

urlpatterns = [
    path('admin/', admin.site.urls),

    # Halaman
    path('', views.landing_page, name='landing'),
    path('peta/jumlah/', views.peta_jumlah, name='peta_jumlah'),
    path('peta/perselisihan/', views.peta_perselisihan, name='peta_perselisihan'),
    path('peta/ekonomi/', views.peta_ekonomi, name='peta_ekonomi'),

    # API GeoJSON
    path('api/geojson/jumlah/', views.api_geojson_jumlah, name='api_geojson_jumlah'),
    path('api/geojson/perselisihan/', views.api_geojson_perselisihan, name='api_geojson_perselisihan'),
    path('api/geojson/ekonomi/', views.api_geojson_ekonomi, name='api_geojson_ekonomi'),
]