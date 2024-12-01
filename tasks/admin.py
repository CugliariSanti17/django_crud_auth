from django.contrib import admin
from .models import Task

class TaskAdmin (admin.ModelAdmin):
    readonly_fields = ('created_at', ) # Especificar que campos son solo lectura
# Register your models here.
admin.site.register(Task, TaskAdmin)