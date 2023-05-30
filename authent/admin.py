from django.contrib import admin
from django.contrib.auth.models import User
from employers.models import Employé

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Employé

class UserAdmin(admin.ModelAdmin):
    model =User 

    fields = ["username"]
    inlines = [ProfileInline]
