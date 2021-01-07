from django.db import models

# Create your models here.
class Patient(models.Model):
    """Пациент"""
    surname = models.CharField('Фамилия', max_length=50)
    name = models.CharField('Имя', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50)

    def __str__(self):
        return self.surname

class Result(models.Model):
    """"Результаты"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blast_cell = models.FloatField('Количество бластных клеток')
    promyelocytes = models.FloatField('Количество милеоцитов')
    neutrophils_myelocytes = models.FloatField('Количество нейтрофилов')
    neutrphils_metamyelocytes = models.FloatField('Нейтрофилы: Миелоциты')

    def __str__(self):
        return str(self.blast_cell)

class Normal_value(models.Model):
    """"Нормальные значения"""
    blast_cell = models.FloatField('Количество бластных клеток', default=0.5)
    promyelocytes = models.FloatField('Количество милеоцитов', default=0.4)
    neutrophils_myelocytes = models.FloatField('Количество нейтрофилов', default=0.3)
    neutrphils_metamyelocytes = models.FloatField('Нейтрофилы: Миелоциты', default=0.2)

    def __str__(self):
        return self.blast_cell

class Deviation(models.Model):
    """"Отклонения"""
    blast_cell = models.FloatField('Количество бластных клеток')
    promyelocytes = models.FloatField('Количество милеоцитов')
    neutrophils_myelocytes = models.FloatField('Количество нейтрофилов')
    neutrphils_metamyelocytes = models.FloatField('Нейтрофилы: Миелоциты')

    def __str__(self):
        return str(self.blast_cell)
