from django.core.management.base import BaseCommand
from security.models import Profile
from faker import Faker
import requests
import io
from django.core.files import File
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data and populate the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating fake data...'))

        def create_fake_user_with_profile():
            # Crie um usuário fictício
            fake_user = User.objects.create_user(
                username=fake.email(),
                password=fake.password(),
                email=fake.email(),
                first_name=fake.first_name(),  # Adicione o primeiro nome fictício
                last_name=fake.last_name(),    # Adicione o sobrenome fictício
            )

            # Verifique se um perfil já existe para este usuário
            existing_profile = Profile.objects.filter(user=fake_user).first()

            if not existing_profile:
                # Crie um perfil fictício associado ao usuário
                profile = Profile.objects.create(user=fake_user)

                # Preencha os campos do perfil com dados fictícios
                profile.bio = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
                profile.phone_number = fake.phone_number()
                profile.birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)

                # Gere um avatar fictício
                avatar_url = fake.image_url(width=200, height=200)
                image_content = requests.get(avatar_url).content
                profile.image.save(f'avatar_{fake_user.username}.jpg', File(io.BytesIO(image_content)), save=True)

        # Crie 50 usuários fictícios com perfis associados
        for _ in range(50):
            create_fake_user_with_profile()

        self.stdout.write(self.style.SUCCESS('Fake data generated successfully.'))
