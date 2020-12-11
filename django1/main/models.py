from django.db import models

# Create your models here.
class table(models.Model):
    title = models.CharField('Название', max_length=50,)

