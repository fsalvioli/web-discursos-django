from django.db import models
from django.urls import reverse

class Persona(models.Model):
    nombre_apellido = models.CharField(max_length=200, unique=True, verbose_name="Nombre y Apeliido")

    def get_absolute_url(self):
        return reverse('register:persona-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.nombre_apellido
    
    # Agrega la relación inversa
    discursos = models.ManyToManyField('Discurso', related_name='personas')

class Discurso(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha = models.DateField()
    tema = models.CharField(max_length=200)
    #cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.persona.nombre_apellido} - {self.fecha}'

