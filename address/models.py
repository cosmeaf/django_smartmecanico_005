from django.db import models
from django.db import models
from django.contrib.auth.models import User
import uuid


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)

    class Meta:
        abstract = True


class Address(Base):
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='addresses')
    cep = models.CharField('CEP', max_length=10)
    logradouro = models.CharField('Logradouro', max_length=255)
    complemento = models.CharField('Complemento', max_length=255, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=255)
    localidade = models.CharField('Cidade', max_length=255)
    uf = models.CharField('Estado', max_length=2)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return self.logradouro

    
