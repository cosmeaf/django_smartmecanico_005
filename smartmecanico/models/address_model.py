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


class Address(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='address')
    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.cep

