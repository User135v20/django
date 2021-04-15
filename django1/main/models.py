from django.db import models
from django.utils import timezone

# Create your models here.

class Patient(models.Model):
    """Пациент"""
    surname = models.CharField('Фамилия', max_length=50)
    name = models.CharField('Имя', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)
    position_at_work = models.CharField('Должность', max_length=50, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.surname

class Image(models.Model):
    """"Изображение"""
    image = models.ImageField("Изображение", upload_to="image/")

    created_at = models.DateTimeField(default=timezone.now)

class Result(models.Model):
    """"Описание снимка"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    structure_asymmetry = models.BooleanField("Ассиметрия пигментации\строения", default=False)
    blue_white_structures = models.BooleanField("Наличие бело-голубых структур", default=False)
    atypical_pigment_network = models.BooleanField("Атипичная пигментная сеть", default=False)
    radial_radiance = models.BooleanField("Радиальная лучистость", default=False)
    points = models.BooleanField("Наличие точек", default=False)

    created_at = models.DateTimeField(default=timezone.now)
class Diagnosis(models.Model):
    """"Предварительный диагноз"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    diagnose = models.CharField('Предварительный диагноз', max_length=150)

    def __str__(self):
        return str(self.id)
