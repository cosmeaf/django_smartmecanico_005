# api/management/commands/generate_fake_addresses.py

from django.core.management.base import BaseCommand
from address.models import Address
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake addresses and associate them with users'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating fake addresses...'))

        def create_fake_address(user):
            # Crie um endereço fictício associado ao usuário
            address = Address.objects.create(
                user=user,
                cep=fake.zipcode(),
                logradouro=fake.street_address(),
                complemento=fake.secondary_address(),
                bairro=fake.word(),
                localidade=fake.city(),
                uf=fake.state_abbr(),
            )

        # Obtenha todos os usuários fictícios
        fake_users = User.objects.all()

        # Associe um endereço fictício a cada usuário fictício
        for fake_user in fake_users:
            create_fake_address(fake_user)

        self.stdout.write(self.style.SUCCESS('Fake addresses generated successfully.'))
