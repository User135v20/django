from django.db import models
from django.utils import timezone

# Create your models here.

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Patient(models.Model, AutoDateTimeField):
    """Пациент"""
    surname = models.CharField('Фамилия', max_length=50)
    name = models.CharField('Имя', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.surname

class Result(models.Model, AutoDateTimeField):
    """"Результаты"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default=None)

    blast_cell = models.FloatField('Количество бластных клеток')
    promyelocytes = models.FloatField('Количество милеоцитов')
    neutrophils_myelocytes = models.FloatField('Количество нейтрофилов')
    neutrphils_metamyelocytes = models.FloatField('Нейтрофилы: Миелоциты')

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.blast_cell)

class Deviation(models.Model):
    """"Отклонения"""
    blast_cell = models.FloatField('Количество бластных клеток')
    promyelocytes = models.FloatField('Количество милеоцитов')
    neutrophils_myelocytes = models.FloatField('Количество нейтрофилов')
    neutrphils_metamyelocytes = models.FloatField('Нейтрофилы: Миелоциты')

    def __str__(self):
        return str(self.blast_cell)
