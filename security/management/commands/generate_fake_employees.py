# api/management/commands/generate_fake_employees.py

from django.core.management.base import BaseCommand
from employee_management.models import Employee, PessoaFisica, PessoaJuridica
from address.models import Address
from faker import Faker
from django.contrib.auth.models import User
from decimal import Decimal


fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake employees and associate them with users and addresses'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating fake employees...'))


        def create_fake_employee():
            # Crie um usuário fictício
            fake_user = User.objects.create_user(
                username=fake.email(),
                password=fake.password(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_staff=True,
            )
            

            # Crie um endereço fictício associado ao usuário
            address = Address.objects.create(
                user=fake_user,
                cep=fake.zipcode(),
                logradouro=fake.street_address(),
                complemento=fake.secondary_address(),
                bairro=fake.word(),
                localidade=fake.city(),
                uf=fake.state_abbr(),
            )

            # Crie um funcionário fictício
            employee = Employee.objects.create(
                type=fake.random_element(elements=('PF', 'PJ')),
                user=fake_user,
            )

            # Preencha os campos do funcionário com dados fictícios
            if employee.type == 'PF':
                PessoaFisica.objects.create(
                    employee=employee,
                    address=address,
                    cpf=fake.unique.random_int(min=10000000000, max=99999999999),
                    rg=fake.unique.random_int(min=100000000, max=999999999),
                    estado_civil=fake.random_element(elements=('solteiro', 'casado', 'divorciado', 'viuvo', 'separado')),
                    genero=fake.random_element(elements=('masculino', 'feminino', 'nao_binario', 'trans_masculino', 'trans_feminino')),
                    salario = Decimal(str(fake.random_int(min=1000, max=10000))) / Decimal('100'),
                    data_admissao=fake.date_between(start_date='-5y', end_date='today'),
                )
            else:
                PessoaJuridica.objects.create(
                    employee=employee,
                    address=address,
                    cnpj=fake.unique.random_int(min=10000000000000, max=99999999999999),
                    razao_social=fake.company(),
                    nome_fantasia=fake.company_suffix(),
                    inscricao_estadual=fake.random_int(min=100000000, max=999999999),
                    inscricao_municipal=fake.random_int(min=100000000, max=999999999),
                    ramo_atividade=fake.catch_phrase(),
                    numero_funcionarios=fake.random_int(min=1, max=100),
                    representante_legal=fake.name(),
                    data_fundacao=fake.date_between(start_date='-30y', end_date='-1y'),
                )

        # Crie 10 funcionários fictícios
        for _ in range(10):
            create_fake_employee()

        self.stdout.write(self.style.SUCCESS('Fake employees generated successfully.'))
