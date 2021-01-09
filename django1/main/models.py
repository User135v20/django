from django.db import models
from django.utils import timezone


# Create your models here.

class Patient(models.Model):
    """Пациент"""
    surname = models.CharField('Фамилия', max_length=50)
    name = models.CharField('Имя', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.surname


class Result(models.Model):
    """"Результаты"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    blast_cell = models.FloatField('Количество бластных клеток')
    blast_cell_deviation = models.FloatField('Количество бластных клеток')
    promyelocytes = models.FloatField('Количество милеоцитов')
    promyelocytes_deviation = models.FloatField('Количество милеоцитов')
    neutrophils_myelocytes = models.FloatField('Количество нейтрофилов')
    neutrophils_myelocytes_deviation = models.FloatField('Количество нейтрофилов')
    neutrphils_metamyelocytes = models.FloatField('Нейтрофилы: Миелоциты')
    neutrphils_metamyelocytes_deviation = models.FloatField('Количество нейтрофилов')

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)
