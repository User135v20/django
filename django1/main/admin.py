from django.contrib import admin
from .models import Patient
from .models import Result
from .models import Deviation
from .models import Normal_value

# Register your models here.
admin.site.register(Patient)
admin.site.register(Result)
admin.site.register(Deviation)
admin.site.register(Normal_value)


