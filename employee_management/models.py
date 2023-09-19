from django.db import models
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('employee_image', filename)

class EmployeeInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)

    cep = models.CharField('CEP', max_length=10)
    logradouro = models.CharField('Logradouro', max_length=255)
    complemento = models.CharField('Complemento', max_length=255, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=255)
    localidade = models.CharField('Cidade', max_length=255)
    uf = models.CharField('Estado', max_length=2)

    CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )
    employee_type = models.CharField(max_length=2, choices=CHOICES, default='PF')

    cpf = models.CharField('CPF', unique=True, blank=True, null=True, max_length=11)
    rg = models.CharField('RG', unique=True, max_length=9, blank=True, null=True)
    
    ESTADO_CIVIL_CHOICES = (
        ('solteiro', 'Solteiro'),
        ('casado', 'Casado'),
        ('divorciado', 'Divorciado'),
        ('viuvo', 'Viúvo'),
        ('separado', 'Separado Judicialmente'),
    )
    estado_civil = models.CharField(max_length=20, blank=True, null=True, choices=ESTADO_CIVIL_CHOICES)
    
    GENERO_CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('nao_binario', 'Não-binário'),
        ('trans_masculino', 'Trans Masculino'),
        ('trans_feminino', 'Trans Feminino'),
        ('agenero', 'Agênero'),
        ('genero_fluido', 'Gênero Fluido'),
        ('two_spirit', 'Two-Spirit'),
        ('homem_cis', 'Homem Cis'),
        ('mulher_cis', 'Mulher Cis'),
        ('nao_informar', 'Prefiro não informar'),
        ('outro', 'Outro'),
    )
    genero = models.CharField(max_length=20, blank=True, null=True, choices=GENERO_CHOICES)

    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField(blank=True, null=True)

    cnpj = models.CharField('CNPJ', unique=True, blank=True, null=True, max_length=14)
    razao_social = models.CharField('Razão Social', max_length=200)
    nome_fantasia = models.CharField('Nome Fantasia', max_length=200)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True)
    ramo_atividade = models.CharField(max_length=255, blank=True, null=True)
    numero_funcionarios = models.PositiveIntegerField('Qtd Funcionários', blank=True, null=True)
    representante_legal = models.CharField(max_length=255, blank=True, null=True)
    data_fundacao = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"



    class Meta:
        verbose_name = 'Recurso Humano'
        verbose_name_plural = 'Recursos Humano'