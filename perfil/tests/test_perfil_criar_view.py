from django.urls import reverse, resolve

from unittest.mock import patch, MagicMock

from perfil import views
from perfil.models import User, Perfil


from produto.tests.test_base import MyBaseTest


class PerfilCriarViewTest(MyBaseTest):
    def mock_authenticate(*args, **kwargs):
        # Retorne um usuário inválido ou None
        return User.objects.none()

    def test_perfil_criar_views_function_is_correct(self):
        view = resolve(
            reverse(
                'perfil:criar'
            )
        )
        self.assertIs(view.func.view_class, views.Criar)

    def test_perfil_criar_views_function_status_code_200_if_method_post(self):
        url = reverse('perfil:criar')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    def test_perfil_criar_views_function_uses_correct_template_if_method_is_get_and_not_authenticated_user(self):  # noqa: E501
        url = reverse('perfil:criar')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'perfil/criar.html')

    def test_perfil_criar_views_function_uses_correct_template_if_method_is_get_and_authenticated_user(self):  # noqa: E501
        user = self.get_auth_data()
        url = reverse('perfil:criar')
        response = self.client.get(url)

        self.assertTrue(user.is_authenticated)
        self.assertTemplateUsed(response, 'perfil/atualizar.html')

    def test_perfil_criar_views_function_show_the_right_context(self):
        url = reverse('perfil:criar')
        response = self.client.get(url)

        self.assertIn('userform', response.context)
        self.assertIn('perfilform', response.context)

    def test_perfil_criar_views_receive_a_valid_form_with_authenticated_user(self):  # noqa: E501
        # criando novo usuario
        new_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # logando ele
        self.client.login(username='testuser', password='testpassword')

        # passando os dados dele no form de criação
        valid = {
            'user_id': '1',
            'username': new_user,
            'idade': 34,
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
        response = self.client.post(url, data=valid, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Você fez login e pode concluir sua compra.')
        self.assertContains(
            response,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

    def test_perfil_criar_views_receive_a_valid_form_with_not_authenticated_user(self):  # noqa: E501
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

        perfil = Perfil.objects.all().first()

        # Agora você pode verificar se a criação do perfil foi bem-sucedida
        # verificando se foi code 200 e se redirecionou pra onde desejo
        self.assertEqual(response.status_code, 200)
        # verificando se a msg de criação de perfil esta existente na pg
        self.assertContains(
            response,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )
        self.assertTrue(perfil)

    def test_perfil_criar_views_receive_a_valid_form_without_password_and_not_authenticated_user(self):  # noqa: E501
        # Dados para o novo usuário sem o campo de senha
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
        # dados de perfil (serao validados pelo userform)
        # sem campo de senha
        perfil = {
            'idade': 34,
            'first_name': 'first',
            'last_name': 'last',
            'username':  'usertest',
            'data_nascimento': '1993-03-21',
            'cpf': '98739945057',
            'email': 'emailzin@test.com',
            'endereco': 'Av. Brasil',
            'numero': '100',
            'complemento': 'A',
            'bairro': 'Centro',
            'cep': '37410045',
            'cidade': 'Cajuru',
            'estado': 'MG'
        }
        # url
        url = reverse('perfil:criar')
        # Crie um mock para o método clean do UserForm
        mock_clean = MagicMock(return_value=None)
        # agora com patch e mock, sera simulado que o formulario passou em
        # todas as validacoes, mesmo sem a senha contida nele.
        with patch('perfil.forms.UserForm.is_valid', return_value=True), \
                patch('perfil.forms.PerfilForm.is_valid', return_value=True), \
        patch('perfil.forms.UserForm.clean', new=mock_clean):   # noqa: E122
            response = self.client.post(
                url,
                data=perfil,
            )

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('produto:carrinho'))

    def test_perfil_criar_views_receive_a_valid_form_without_password_and_is_authenticated_user(self):  # noqa: E501
        # criando novo usuario
        new_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # logando ele
        self.client.login(username='testuser', password='testpassword')

        # passando os dados dele no form de criação, sem a senha
        valid = {
            'user_id': '1',
            'username': new_user,
            'idade': 34,
            'data_nascimento': '1993-03-21',
            'cpf': '98739945057',
            'email': 'emailzin@test.com',
            'endereco': 'Av. Brasil',
            'numero': '100',
            'complemento': 'A',
            'bairro': 'Centro',
            'cep': '37410045',
            'cidade': 'Cajuru',
            'estado': 'MG'
        }

        url = reverse('perfil:criar')
        # Crie um mock para o método clean do UserForm
        mock_clean = MagicMock(return_value=None)
        # agora com patch e mock, sera simulado que o formulario passou em
        # todas as validacoes, mesmo sem a senha contida nele.
        with patch('perfil.forms.UserForm.is_valid', return_value=True), \
                patch('perfil.forms.PerfilForm.is_valid', return_value=True), \
        patch('perfil.forms.UserForm.clean', new=mock_clean):   # noqa: E122
            response = self.client.post(
                url,
                data=valid,
            )

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('produto:carrinho'))

    def test_perfil_criar_view_dont_find_user_return_404(self):
        self.make_perfil()

        url = reverse('perfil:criar')

        # passando os dados dele no form de criação
        valid = {
            'user_id': '1',
            'username': 'new_user',
            'idade': 34,
            'data_nascimento': '1993-03-21',
            'cpf': '98739945057',
            'email': 'emailzin@test.com',
            'password': '123456',
            'password2': '123456',
            'endereco': 'Av. Brasil',
            'numero': '100',
            'complemento': 'A',
            'bairro': 'Centro',
            'cep': '37410045',
            'cidade': 'Cajuru',
            'estado': 'MG'
        }

        response = self.client.post(url, data=valid)
        self.assertEqual(response.status_code, 404)

    def test_perfil_criar_view_receive_valid_form_and_already_have_a_perfil(self):  # noqa: E501
        # criando novo usuario
        new_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # logando ele
        self.client.login(username='testuser', password='testpassword')
        valid = {
            'user_id': '1',
            'username': new_user,
            'idade': 34,
            'data_nascimento': '1993-03-21',
            'cpf': '98739945057',
            'email': 'emailzin@test.com',
            'password': '123456',
            'password2': '123456',
            'endereco': 'Av. Brasil',
            'numero': '100',
            'complemento': 'A',
            'bairro': 'Centro',
            'cep': '37410045',
            'cidade': 'Cajuru',
            'estado': 'MG'
        }
        perfil = Perfil.objects.create(
            user=new_user,
            idade=34,
            data_nascimento='1993-03-21',
            cpf='98739945057',
            endereco='Av. Brasil',
            numero='100',
            complemento='A',
            bairro='Centro',
            cep='37410045',
            cidade='Cajuru',
            estado='MG')
        perfil.save()
        url = reverse('perfil:criar')
        response = self.client.post(url, data=valid, follow=True)
        # checando se redirecionou pro local certo
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('produto:carrinho'))
        # checando as msg
        self.assertIn(
            'Seu cadastro foi criado ou atualizado com sucesso.',
            response.content.decode('utf-8')
        )
        self.assertIn(
            'Você fez login e pode concluir sua compra.',
            response.content.decode('utf-8')
        )
