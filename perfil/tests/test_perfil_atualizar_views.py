from django.urls import reverse, resolve

from perfil import views

from produto.tests.test_base import MyBaseTest


class PerfilAtualizarViewTest(MyBaseTest):
    def test_perfil_atualizar_view_function_is_correct(self):
        view = resolve(
            reverse('perfil:atualizar')
        )
        self.assertIs(view.func.view_class, views.Atualizar)

    def test_perfil_atualizar_view_status_code_200_if_method_get(self):
        url = reverse('perfil:atualizar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_perfil_atualizar_view_status_code_405_if_method_post(self):
        url = reverse('perfil:atualizar')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_atualizar_view_status_code_405_if_method_put(self):
        url = reverse('perfil:atualizar')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_atualizar_view_status_code_405_if_method_patch(self):
        url = reverse('perfil:atualizar')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_atualizar_view_status_code_405_if_method_delete(self):
        url = reverse('perfil:atualizar')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_atualizar_view_return_atualizar(self):
        url = reverse('perfil:atualizar')
        response = self.client.get(url)
        self.assertContains(response, 'Atualizar')
