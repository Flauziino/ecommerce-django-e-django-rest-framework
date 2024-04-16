from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from perfil.forms import UserForm

from unittest.mock import patch


class PerfilUserFomrmTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.new_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

        self.perfil_data = {
            'idade': 34,
            'first_name': 'first',
            'last_name': 'last',
            'username':  'usertest',
            'data_nascimento': '1993-03-21',
            'cpf': '98739945057',
            'email': 'emailzin@test.com',
            'endereco': 'Av. Brasil',
            'password': '123456',
            'password2': '123456',
            'numero': '100',
            'complemento': 'A',
            'bairro': 'Centro',
            'cep': '37410045',
            'cidade': 'Cajuru',
            'estado': 'MG'
        }

    def test_userform_password_field_label_is_correct(self):
        form = UserForm()
        label = form['password'].field.label
        self.assertEqual(label, 'Senha')

    def test_userform_password2_field_label_is_correct(self):
        form = UserForm()
        label = form['password2'].field.label
        self.assertEqual(label, 'Confirmação senha')

    def test_user_form_password_and_password2_field_is_required_not_authenticated_user(self):  # noqa: E501
        data = self.perfil_data
        data['password'] = ''
        data['password2'] = ''

        url = reverse('perfil:criar')

        response = self.client.post(url, data=data)
        self.assertIn(
            'Este campo é obrigatório.',
            response.content.decode('utf-8')
        )

    def test_user_form_password_and_password2_field_need_to_match_not_authenticated_user(self):  # noqa: E501
        data = self.perfil_data
        data['password'] = '123'
        data['password2'] = '321'

        url = reverse('perfil:criar')

        response = self.client.post(url, data=data)
        self.assertIn(
            'As duas senhas não conferem',
            response.content.decode('utf-8')
        )

    def test_user_form_password_and_password2_need_at_least_6_chars_not_authenticated_user(self):  # noqa: E501
        data = self.perfil_data
        data['password'] = '123'
        data['password2'] = '123'

        url = reverse('perfil:criar')

        response = self.client.post(url, data=data)
        self.assertIn(
            'Sua senha precisa de pelo menos 6 caracteres',
            response.content.decode('utf-8')
        )

    def test_user_form_username_field_already_taken_not_authenticated_user(self):  # noqa: E501
        # criando user para simular que seus dados ja existem no bd
        new_user = self.new_user_data
        user = User.objects.create_user(**new_user)
        # salvando user
        user.save()

        url = reverse('perfil:criar')
        # pegando a primeira resposta
        response = self.client.post(url, data=self.perfil_data, follow=True)
        # verificando se o cadastro foi criado com sucesso
        self.assertIn(
            'Seu cadastro foi criado ou atualizado com sucesso.',
            response.content.decode('utf-8')
        )
        # realizando logout antes de iniciar o proximo teste
        self.client.logout()
        # iniciando de fato os testes
        # pegando novamente os dados
        data = self.perfil_data
        # alterando o email para um email que nao exista para n levantar
        # o erro do campo email.
        data['email'] = 'anotheremailfortest@email.com'
        # passando um username igual o ja existente
        data['username'] = 'testuser'
        test_response = self.client.post(url, data=data, follow=True)
        # verificando a msg de usuario existente
        self.assertIn(
            'Usuário já existe',
            test_response.content.decode('utf-8')
        )

    def test_user_form_email_field_already_taken_not_authenticated_user(self):
        # criando user para simular que seus dados ja existem no bd
        new_user = self.new_user_data
        user = User.objects.create_user(**new_user)
        # salvando user
        user.save()

        url = reverse('perfil:criar')
        # pegando a primeira resposta
        response = self.client.post(url, data=self.perfil_data, follow=True)
        # verificando se o cadastro foi criado com sucesso
        self.assertIn(
            'Seu cadastro foi criado ou atualizado com sucesso.',
            response.content.decode('utf-8')
        )
        # realizando logout antes de iniciar o proximo teste
        self.client.logout()
        # iniciando de fato os testes
        # pegando novamente os dados
        data = self.perfil_data
        # alterando o email para um email ja existente
        data['email'] = 'test@example.com'
        # passando um username diferente para nao levantar o erro
        # de usuario
        data['username'] = 'helloo_test'
        test_response = self.client.post(url, data=data, follow=True)
        # verificando a msg de usuario existente
        self.assertIn(
            'E-mail já existe',
            test_response.content.decode('utf-8')
        )

    def test_user_form_password_and_password2_field_need_to_match_authenticated_user(self):  # noqa: E501
        # criando user para simular que seus dados ja existem no bd
        new_user = self.new_user_data
        user = User.objects.create_user(**new_user)
        # salvando user
        user.save()

        url = reverse('perfil:criar')
        # pegando a primeira resposta
        response = self.client.post(url, data=self.perfil_data, follow=True)
        # verificando se o cadastro foi criado com sucesso
        self.assertIn(
            'Seu cadastro foi criado ou atualizado com sucesso.',
            response.content.decode('utf-8')
        )
        self.client.force_login(user)
        # iniciando de fato os testes
        # pegando novamente os dados
        data = self.perfil_data
        data['password'] = '123456'
        data['password2'] = '132452'
        test_response = self.client.post(url, data=data, follow=True)
        # verificando a msg de usuario existente
        self.assertIn(
            'As duas senhas não conferem',
            test_response.content.decode('utf-8')
        )

    def test_user_form_password_field_too_short_need_more_than_6_chars(self):
        # criando user para simular que seus dados ja existem no bd
        new_user = self.new_user_data
        user = User.objects.create_user(**new_user)
        # salvando user
        user.save()

        url = reverse('perfil:criar')
        # pegando a primeira resposta
        response = self.client.post(url, data=self.perfil_data, follow=True)
        # verificando se o cadastro foi criado com sucesso
        self.assertIn(
            'Seu cadastro foi criado ou atualizado com sucesso.',
            response.content.decode('utf-8')
        )
        self.client.force_login(user)
        # iniciando de fato os testes
        # pegando novamente os dados
        data = self.perfil_data
        data['password'] = '123'
        data['password2'] = '123'
        test_response = self.client.post(url, data=data, follow=True)
        # verificando a msg de usuario existente
        self.assertIn(
            'Sua senha precisa de pelo menos 6 caracteres',
            test_response.content.decode('utf-8')
        )

    @patch('django.contrib.auth.models.User.objects.filter')
    def test_user_form_email_field_already_taken(self, mock_email_filter):
        # criando user para simular que seus dados ja existem no bd
        new_user = self.new_user_data
        user = User.objects.create_user(**new_user)
        # salvando user
        user.save()

        url = reverse('perfil:criar')
        self.client.force_login(user)

        # configurando mock para retornar um email existente
        mock_email_filter.return_value.first.return_value = User(
            email='test@example.com'
        )

        # iniciando de fato os testes
        # pegando novamente os dados
        data = self.perfil_data
        data['email'] = 'emailzin@test.com'
        data['cpf'] = '90475204085'
        test_response = self.client.post(url, data=data, follow=True)
        # configurando mock para retornar um email existente
        mock_email_filter.return_value.first.return_value = User(
            email='test@example.com'
        )
        # verificando a msg de usuario existente
        self.assertIn(
            'E-mail já existe',
            test_response.content.decode('utf-8')
        )

    def test_user_form_dont_receive_a_password_with_authenticated_user(self):
        # criando user para simular que seus dados ja existem no bd
        new_user = self.new_user_data
        user = User.objects.create_user(**new_user)
        # salvando user
        user.save()

        url = reverse('perfil:criar')
        # pegando a primeira resposta
        response = self.client.post(url, data=self.perfil_data, follow=True)
        # verificando se o cadastro foi criado com sucesso
        self.assertIn(
            'Seu cadastro foi criado ou atualizado com sucesso.',
            response.content.decode('utf-8')
        )
        self.client.force_login(user)
        # iniciando de fato os testes
        # pegando novamente os dados
        data = self.perfil_data
        data['password'] = ''
        data['password2'] = ''
        data['cpf'] = '90475204085'
        test_response = self.client.post(url, data=data, follow=True)
        # verificando a msg de usuario existente
        self.assertIn(
            'Seu cadastro foi criado ou atualizado com sucesso.',
            test_response.content.decode('utf-8')
        )
