from django.contrib import admin
from .models import Employé, Spécialité, Siege
# Register your models here.
admin.site.register(Employé)
admin.site.register(Spécialité)
admin.site.register(Siege)