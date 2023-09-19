# api/management/commands/generate_fake_vehicles.py

from django.core.management.base import BaseCommand
from vehicle.models import Vehicle
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake vehicles and associate them with users'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating fake vehicles...'))

        def create_fake_vehicle(user):
            # Crie um veículo fictício associado ao usuário
            vehicle = Vehicle.objects.create(
                user=user,
                brand=fake.company(),
                model=fake.word(),
                fuel=fake.word(),
                year=fake.year(),
                odometer=fake.random_int(min=0, max=200000),
                plate=fake.license_plate(),
            )

        # Obtenha todos os usuários fictícios
        fake_users = User.objects.all()

        # Associe um veículo fictício a cada usuário fictício
        for fake_user in fake_users:
            create_fake_vehicle(fake_user)

        self.stdout.write(self.style.SUCCESS('Fake vehicles generated successfully.'))
