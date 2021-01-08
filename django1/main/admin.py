from django.contrib import admin
from .models import Patient
from .models import Result
from .models import Deviation

# Register your models here.
admin.site.register(Patient)
admin.site.register(Result)
admin.site.register(Deviation)


