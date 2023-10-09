# Generated by Django 4.2.5 on 2023-10-09 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('cep', models.CharField(max_length=10, verbose_name='CEP')),
                ('logradouro', models.CharField(max_length=255, verbose_name='Logradouro')),
                ('complemento', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=255, verbose_name='Bairro')),
                ('localidade', models.CharField(max_length=255, verbose_name='Cidade')),
                ('uf', models.CharField(max_length=2, verbose_name='Estado')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
    ]
