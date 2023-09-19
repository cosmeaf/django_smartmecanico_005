from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Address

class AddressAPITestCase(TestCase):
    def setUp(self):
        # Criar um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Criar um cliente de teste
        self.client = Client()

        # Logar com o usuário de teste
        self.client.login(username='testuser', password='testpassword')

        # Criar um endereço de teste
        self.address = Address.objects.create(
            cep='12345678',
            logradouro='Test Street',
            complemento='123A',
            bairro='Test Borough',
            localidade='Test City',
            uf='TS',
            user=self.user,
        )
        
    def test_get_addresses(self):
        # Realizar uma requisição GET para a API de endereços
        response = self.client.get('/api/addresses/')

        # Verificar se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a resposta contém o endereço criado
        self.assertContains(response, '12345678')
        
    def test_create_address(self):
        # Dados para a criação de um novo endereço
        new_address_data = {
            'cep': '87654321',
            'logradouro': 'New Street',
            'complemento': '321B',
            'bairro': 'New Borough',
            'localidade': 'New City',
            'uf': 'NS',
        }
        
        # Realizar uma requisição POST para criar um novo endereço
        response = self.client.post('/api/addresses/', data=new_address_data)
        
        # Verificar se a resposta tem status code 201 (Created)
        self.assertEqual(response.status_code, 201)
        
        # Verificar se o novo endereço foi criado corretamente
        self.assertContains(response, '87654321')
