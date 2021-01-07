# Generated by Django 3.1.3 on 2021-01-04 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deviation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blast_cell', models.FloatField(verbose_name='Количество бластных клеток')),
                ('promyelocytes', models.FloatField(verbose_name='Количество милеоцитов')),
                ('neutrophils_myelocytes', models.FloatField(verbose_name='Количество нейтрофилов')),
                ('neutrphils_metamyelocytes', models.FloatField(verbose_name='Нейтрофилы: Миелоциты')),
            ],
        ),
        migrations.CreateModel(
            name='Normal_values',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blast_cell', models.FloatField(default=0.5, verbose_name='Количество бластных клеток')),
                ('promyelocytes', models.FloatField(default=0.4, verbose_name='Количество милеоцитов')),
                ('neutrophils_myelocytes', models.FloatField(default=0.3, verbose_name='Количество нейтрофилов')),
                ('neutrphils_metamyelocytes', models.FloatField(default=0.2, verbose_name='Нейтрофилы: Миелоциты')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blast_cell', models.FloatField(verbose_name='Количество бластных клеток')),
                ('promyelocytes', models.FloatField(verbose_name='Количество милеоцитов')),
                ('neutrophils_myelocytes', models.FloatField(verbose_name='Количество нейтрофилов')),
                ('neutrphils_metamyelocytes', models.FloatField(verbose_name='Нейтрофилы: Миелоциты')),
            ],
        ),
    ]