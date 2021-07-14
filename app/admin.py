from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(student)
class AdminStudent(admin.ModelAdmin):
    list_display =[field.name for field in student._meta.fields]