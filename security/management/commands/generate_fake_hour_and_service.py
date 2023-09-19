import json
from django.core.management.base import BaseCommand
from services.models import Service, HourService
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()
superuser='cosmeaf@gmail.com'

class Command(BaseCommand):
    help = 'Generate fake services and hours and associate them with a specific superuser'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating fake services and hours...'))

        def create_fake_service_and_hours(user):
            try:
                # Limpar os dados existentes
                Service.objects.filter(user=user).delete()
                HourService.objects.filter(user=user).delete()

                # Definindo o caminho exato para o arquivo JSON
                file_path = 'security/management/json/services_data.json'

                # Ler os dados de serviços do JSON
                with open(file_path, 'r') as f:
                    services_data = json.load(f)

                # Criar serviços falsos
                for service_data in services_data:
                    Service.objects.create(
                        user=user,
                        name=service_data['name'],
                        description=service_data['description'],
                    )

                # Criar horas falsas de serviço
                hours = [
                    "08:00", "09:00", "10:00", "11:00",
                    "12:00", "13:00", "14:00", "15:00",
                    "16:00", "17:00"
                ]

                for hour_str in hours:
                    HourService.objects.create(
                        user=user,
                        hour=hour_str,
                    )
            
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR('O arquivo JSON não foi encontrado.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ocorreu um erro inesperado: {e}'))

        try:
            # Obtenha o superuser específico
            user = User.objects.get(email=superuser)
            create_fake_service_and_hours(user)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Superuser com o email especificado não encontrado.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro inesperado: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Fake services and hours generated successfully.'))
