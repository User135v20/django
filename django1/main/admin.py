from django.contrib import admin
from .models import User
from .models import Result
from .models import Image

# Register your models here.
admin.site.register(User)
admin.site.register(Result)
admin.site.register(Image)


