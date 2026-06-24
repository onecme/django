"""
Script seeder — jalankan dari root proyek:

    cd D:\\django\\sig\\projek_kelompok
    python -m webPerceraian_indonesia.seed_perceraian
"""

import os
import sys
import json
import csv
import django

# Bootstrap Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webPerceraian_indonesia.settings')
django.setup()

from webPerceraian_indonesia.models import Provinsi, DataPerceraian

BASE = os.path.dirname(os.path.abspath(__file__))
GEOJSON_PATH = os.path.join(BASE, 'data', '38 Provinsi Indonesia - Provinsi.json')
CSV_PATH     = os.path.join(BASE, 'data', 'Jumlah Perceraian Menurut Provinsi dan Faktor, 2023_final.csv')

NAMA_MAP = {
    "Aceh": "Aceh",
    "Sumatera Utara": "Sumatera Utara",
    "Sumatera Barat": "Sumatera Barat",
    "Riau": "Riau",
    "Jambi": "Jambi",
    "Sumatera Selatan": "Sumatera Selatan",
    "Bengkulu": "Bengkulu",
    "Lampung": "Lampung",
    "Kepulauan Bangka Belitung": "Kepulauan Bangka Belitung",
    "Kepulauan Riau": "Kepulauan Riau",
    "DKI Jakarta": "DKI Jakarta",
    "Jawa Barat": "Jawa Barat",
    "Jawa Tengah": "Jawa Tengah",
    "DI Yogyakarta": "Daerah Istimewa Yogyakarta",
    "Jawa Timur": "Jawa Timur",
    "Banten": "Banten",
    "Bali": "Bali",
    "Nusa Tenggara Barat": "Nusa Tenggara Barat",
    "Nusa Tenggara Timur": "Nusa Tenggara Timur",
    "Kalimantan Barat": "Kalimantan Barat",
    "Kalimantan Tengah": "Kalimantan Tengah",
    "Kalimantan Selatan": "Kalimantan Selatan",
    "Kalimantan Timur": "Kalimantan Timur",
    "Kalimantan Utara": "Kalimantan Utara",
    "Sulawesi Utara": "Sulawesi Utara",
    "Sulawesi Tengah": "Sulawesi Tengah",
    "Sulawesi Selatan": "Sulawesi Selatan",
    "Sulawesi Tenggara": "Sulawesi Tenggara",
    "Gorontalo": "Gorontalo",
    "Sulawesi Barat": "Sulawesi Barat",
    "Maluku": "Maluku",
    "Maluku Utara": "Maluku Utara",
    "Papua Barat": "Papua Barat",
    "Papua": "Papua",
}

PROVINSI_SKIP = {"Papua Barat Daya", "Papua Selatan", "Papua Tengah", "Papua Pegunungan", "Indonesia"}

def run():
    print("📂 Membaca GeoJSON...")
    with open(GEOJSON_PATH, encoding='utf-8') as f:
        geojson = json.load(f)

    geo_dict = {}
    for feat in geojson['features']:
        p = feat['properties']
        geo_dict[p['PROVINSI'].strip()] = {
            'kode': p['KODE_PROV'],
            'geometry': feat['geometry'],
        }
    print(f"✅ {len(geo_dict)} polygon dimuat")

    print("📂 Membaca CSV...")
    csv_data = {}
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            nama = row['Provinsi'].strip()
            if nama in PROVINSI_SKIP or not nama:
                continue
            try:
                csv_data[nama] = {
                    'jumlah':       int(row['Fakor Perceraian - Jumlah'].strip()),
                    'perselisihan': int(row['Fakor Perceraian - Perselisihan dan Pertengkaran Terus Menerus'].strip()),
                    'ekonomi':      int(row['Fakor Perceraian - Ekonomi'].strip()),
                }
            except ValueError:
                print(f"⚠️  Skip {nama} (data tidak valid)")
    print(f"✅ {len(csv_data)} baris CSV dimuat")

    created_prov = created_data = skipped = 0
    for nama_csv, angka in csv_data.items():
        nama_geo = NAMA_MAP.get(nama_csv)
        if not nama_geo:
            print(f"⚠️  Tidak ada mapping: '{nama_csv}'")
            skipped += 1
            continue
        geo = geo_dict.get(nama_geo)
        if not geo:
            print(f"⚠️  Polygon tidak ada: '{nama_geo}'")
            skipped += 1
            continue

        prov, pc = Provinsi.objects.update_or_create(
            kode_prov=geo['kode'],
            defaults={'nama': nama_geo, 'geometry': geo['geometry']}
        )
        if pc: created_prov += 1

        _, dc = DataPerceraian.objects.update_or_create(
            provinsi=prov,
            defaults={
                'tahun': 2023,
                'jumlah_perceraian': angka['jumlah'],
                'faktor_perselisihan': angka['perselisihan'],
                'faktor_ekonomi': angka['ekonomi'],
            }
        )
        if dc: created_data += 1

    print(f"\n🎉 Selesai! Provinsi baru: {created_prov} | Data baru: {created_data} | Skip: {skipped}")

if __name__ == '__main__':
    run()