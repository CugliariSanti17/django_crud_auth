from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task (models.Model):
    title = models.CharField(max_length=200) # Texto
    description = models.TextField(blank=True, max_length=500) #Texto
    created_at = models.DateTimeField(auto_now_add=True)#Fecha
    datecompleted = models.DateTimeField(null=True, blank=True) #Fecha
    important = models.BooleanField(default=False)#Checkbox
    user = models.ForeignKey(User, on_delete=models.CASCADE)#Conectar con otra tabla (User)
    
    def __str__(self): # Mostrar el titulo en el panel de administrador
        return self.title + '- by' + self.user.username
    
