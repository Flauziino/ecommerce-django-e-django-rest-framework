from django.urls import reverse, resolve

from perfil import views
from perfil.models import User


from produto.tests.test_base import MyBaseTest


class PerfilLoginViewTest(MyBaseTest):

    def test_perfil_login_views_function_is_correct(self):
        view = resolve(
            reverse(
                'perfil:login'
            )
        )
        self.assertIs(view.func.view_class, views.Login)

    def test_perfil_login_views_returns_status_code_405_if_method_get(self):
        url = reverse('perfil:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_login_views_returns_status_code_405_if_method_patch(self):
        url = reverse('perfil:login')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_login_views_returns_status_code_405_if_method_put(self):
        url = reverse('perfil:login')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_login_views_returns_status_code_405_if_method_delete(self):
        url = reverse('perfil:login')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_login_views_function_success_login_user(self):
        # Dados para o novo usuário
        new_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        # Criar um novo usuário
        new_user = User.objects.create_user(**new_user_data)
        new_user.save()
        # Dados para criar um perfil
        perfil_data = {
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
        url = reverse('perfil:criar')
        response = self.client.post(url, data=perfil_data, follow=True)

        # Agora você pode verificar se a criação do perfil foi bem-sucedida
        # verificando se foi code 200 e se redirecionou pra onde desejo
        self.assertEqual(response.status_code, 200)
        # verificando se a msg de criação de perfil esta existente na pg
        self.assertContains(
            response,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        # INICIANDO a fonfiguração para o teste.
        url = reverse('perfil:login')
        response = self.client.post(
            url,
            data={
                'username': 'usertest',
                'password': '123456'
            }, follow=True
        )
        # verificando se seguiu a url corretamente
        self.assertEqual(response.status_code, 200)
        # verificando se seguiu para a url esperada
        self.assertRedirects(response, reverse('produto:carrinho'))
        # verificando se a msg de sucesso esta na pg
        self.assertContains(
            response,
            'Você fez login no sistema e pode concluir sua compra.'
        )

    def test_perfil_login_views_function_fails_to_authenticate_user_wrong_credentials(self):  # noqa: E501
        # Dados para o novo usuário
        new_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        # Criar um novo usuário
        new_user = User.objects.create_user(**new_user_data)
        new_user.save()
        # Dados para criar um perfil
        perfil_data = {
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
        url = reverse('perfil:criar')
        response = self.client.post(url, data=perfil_data, follow=True)

        # Agora você pode verificar se a criação do perfil foi bem-sucedida
        # verificando se foi code 200 e se redirecionou pra onde desejo
        self.assertEqual(response.status_code, 200)
        # verificando se a msg de criação de perfil esta existente na pg
        self.assertContains(
            response,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        # INICIANDO a fonfiguração para o teste.
        url = reverse('perfil:login')
        response = self.client.post(
            url,
            data={
                'username': 'usertest',
                'password': 'wrong'
            }, follow=True
        )
        # verificando se seguiu o redirect
        self.assertEqual(response.status_code, 200)
        # verificando se deu redirect para pagina correta
        self.assertRedirects(response, reverse('perfil:criar'))
        # verificando a msg de erro
        self.assertContains(
            response,
            'Usuário ou senha inválidos.'
        )

    def test_perfil_login_views_function_fails_to_authenticate_user_missing_credentials(self):  # noqa: E501
        # Dados para o novo usuário
        new_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        # Criar um novo usuário
        new_user = User.objects.create_user(**new_user_data)
        new_user.save()
        # Dados para criar um perfil
        perfil_data = {
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
        url = reverse('perfil:criar')
        response = self.client.post(url, data=perfil_data, follow=True)

        # Agora você pode verificar se a criação do perfil foi bem-sucedida
        # verificando se foi code 200 e se redirecionou pra onde desejo
        self.assertEqual(response.status_code, 200)
        # verificando se a msg de criação de perfil esta existente na pg
        self.assertContains(
            response,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        # INICIANDO a fonfiguração para o teste.
        url = reverse('perfil:login')
        response = self.client.post(
            url,
            data={
                'username': '',
                'password': 'wrong'
            }, follow=True
        )
        # verificando se seguiu a url corretamente
        self.assertEqual(response.status_code, 200)
        # verificando se redireciounou para pg esperada
        self.assertRedirects(response, reverse('perfil:criar'))
        # verificando se a msg de erro esta contida na pg
        self.assertContains(
            response,
            'Usuário ou senha inválidos.'
        )
