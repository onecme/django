
from django.db import models


class Province(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    alt_name = models.CharField(max_length=255, default="", blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        db_table = "provinces"
        managed = True  # set False kalau tabel sudah ada dan tidak mau dimigrasi

    def __str__(self):
        return self.name
    

class Regency(models.Model):
    id = models.BigIntegerField(primary_key=True)

    province = models.ForeignKey(
        "Province",
        on_delete=models.CASCADE,
        db_column="province_id",
        related_name="regencies"
    )

    name = models.CharField(max_length=255)
    alt_name = models.CharField(max_length=255, default="", blank=True)

    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        db_table = "regencies"
        managed = True  # ubah ke False kalau tabel sudah ada di PostgreSQL

    def __str__(self):
        return self.name
    

class District(models.Model):
    id = models.BigIntegerField(primary_key=True)

    regency = models.ForeignKey(
        "Regency",
        on_delete=models.CASCADE,
        db_column="regency_id",
        related_name="districts"
    )

    name = models.CharField(max_length=255)
    alt_name = models.CharField(max_length=255, default="", blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        db_table = "districts"
        managed = True

    def __str__(self):
        return self.name


class NamaData(models.Model):
    # Django secara otomatis membuat field 'id' sebagai AutoField (Integer) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Datprof(models.Model):
    # Menggunakan AutoField bawaan Django untuk id/primary key tabel ini
    province = models.ForeignKey(
        "Province",
        on_delete=models.CASCADE,
        db_column="province_id",
        related_name="datprof_provinces"
    )
    nama = models.ForeignKey(
        "NamaData",
        on_delete=models.CASCADE,
        db_column="nama_id",
        related_name="datprof_nama"
    )
    tahun = models.IntegerField()
    jumlah = models.FloatField()  # Double precision di PostgreSQL dipetakan ke FloatField

    class Meta:
        db_table = "data_provinces"
        managed = True

    def __str__(self):
        return f"{self.province.name} - {self.nama.name} ({self.tahun})"