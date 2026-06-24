# Setup Proyek Django – Web Perceraian Indonesia

## Struktur File yang Dihasilkan

```
webPerceraian_indonesia/
├── webPerceraian_indonesia/
│   ├── urls.py          ← (ganti dengan urls.py yang diberikan)
│   └── settings.py
├── perceraian/          ← nama app (sesuaikan jika berbeda)
│   ├── models.py        ← (salin dari models.py yang diberikan)
│   ├── views.py         ← (salin dari views.py yang diberikan)
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── seed_perceraian.py   ← (salin file seeder)
├── templates/
│   ├── landing.html     ← (sudah ada)
│   └── peta.html        ← (salin dari peta.html yang diberikan)
└── data/
    ├── 38_Provinsi_Indonesia_-_Provinsi.json
    └── Jumlah_Perceraian_Menurut_Provinsi_dan_Faktor__2023_final.csv
```

---

## 1. Konfigurasi settings.py

```python
# settings.py

INSTALLED_APPS = [
    ...
    'django.contrib.postgres',  # WAJIB untuk JSONField + PostgreSQL
    'perceraian',               # nama app Anda
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_perceraian',       # Ganti sesuai nama database Anda
        'USER': 'postgres',            # Ganti sesuai user PostgreSQL
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],   # Pastikan ini ada
        ...
    },
]
```

---

## 2. Buat Database PostgreSQL

```bash
# Di terminal PostgreSQL
psql -U postgres
CREATE DATABASE db_perceraian;
\q
```

---

## 3. Install Dependensi

```bash
pip install django psycopg2-binary
```

---

## 4. Salin File ke Proyek

```bash
# Salin models.py ke app
cp models.py perceraian/models.py

# Salin views.py ke app
cp views.py perceraian/views.py

# Salin template peta
cp peta.html templates/peta.html

# Buat folder management command
mkdir -p perceraian/management/commands
touch perceraian/management/__init__.py
touch perceraian/management/commands/__init__.py
cp seed_perceraian.py perceraian/management/commands/seed_perceraian.py

# Buat folder data
mkdir -p data
cp /path/to/38_Provinsi_Indonesia_-_Provinsi.json data/
cp /path/to/Jumlah_Perceraian_Menurut_Provinsi_dan_Faktor__2023_final.csv data/
```

---

## 5. Sesuaikan Import di views.py dan seed_perceraian.py

Ganti semua `from perceraian.models import` dengan nama app Anda yang sebenarnya.
Juga ganti `from perceraian import views` di `urls.py`.

---

## 6. Migrasi Database

```bash
python manage.py makemigrations perceraian
python manage.py migrate
```

---

## 7. Jalankan Seeder

```bash
python manage.py seed_perceraian
```

Output yang diharapkan:
```
📂 Membaca GeoJSON...
✅ 38 polygon provinsi dimuat dari GeoJSON
📂 Membaca CSV BPS...
✅ 34 baris CSV perceraian dimuat

🎉 Seeder selesai!
   Provinsi baru: 34
   Data perceraian baru: 34
   Dilewati: 0
```

---

## 8. Tambahkan ke Admin (opsional)

```python
# perceraian/admin.py
from django.contrib import admin
from .models import Provinsi, DataPerceraian

@admin.register(Provinsi)
class ProvinsiAdmin(admin.ModelAdmin):
    list_display = ['kode_prov', 'nama']
    search_fields = ['nama']

@admin.register(DataPerceraian)
class DataPerceraianAdmin(admin.ModelAdmin):
    list_display = ['provinsi', 'tahun', 'jumlah_perceraian', 'faktor_perselisihan', 'faktor_ekonomi']
    search_fields = ['provinsi__nama']
```

---

## 9. Jalankan Server

```bash
python manage.py runserver
```

Akses di:
- `http://localhost:8000/`                  → Landing Page
- `http://localhost:8000/peta/jumlah/`      → Heatmap Total Perceraian
- `http://localhost:8000/peta/perselisihan/`→ Heatmap Faktor Perselisihan
- `http://localhost:8000/peta/ekonomi/`     → Heatmap Faktor Ekonomi
- `http://localhost:8000/api/geojson/jumlah/`    → API GeoJSON (JSON)

---

## Catatan Penting

**Provinsi dengan data "..." di CSV (pemekaran baru 2022):**
- Papua Barat Daya
- Papua Selatan
- Papua Tengah
- Papua Pegunungan

Keempat provinsi ini ada di GeoJSON (tampil di peta) tetapi tidak punya data
perceraian di CSV BPS 2023. Seeder akan skip dan provinsi-provinsi ini tidak
dimasukkan ke database. Polygonnya tidak akan muncul di peta (tidak ada di
FeatureCollection yang dikembalikan API).

Jika ingin tetap ditampilkan di peta dengan nilai 0, modifikasi seeder untuk
memasukkan mereka dengan nilai 0, dan API view tetap akan include mereka.
