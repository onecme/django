from django.db import models


class Provinsi(models.Model):
    kode_prov = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=100, unique=True)
    geometry = models.JSONField()

    class Meta:
        db_table = "provinsi"
        ordering = ["nama"]

    def __str__(self):
        return self.nama


class DataPerceraian(models.Model):
    provinsi = models.OneToOneField(
        Provinsi,
        on_delete=models.CASCADE,
        related_name="data_perceraian"
    )
    tahun = models.PositiveSmallIntegerField(default=2023)
    jumlah_perceraian = models.IntegerField()
    faktor_perselisihan = models.IntegerField()
    faktor_ekonomi = models.IntegerField()

    class Meta:
        db_table = "data_perceraian"

    def __str__(self):
        return f"{self.provinsi.nama} ({self.tahun})"