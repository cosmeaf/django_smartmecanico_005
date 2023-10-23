from django.db import models
from security.models import CustomUser
import uuid

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)

    class Meta:
        abstract = True

class Vehicle(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicles')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    fuel = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    odometer = models.CharField(max_length=20)
    plate = models.CharField(max_length=15, unique=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['-deleted_at', '-updated_at', 'year', 'brand', 'plate']

    def __str__(self):
        return self.plate

