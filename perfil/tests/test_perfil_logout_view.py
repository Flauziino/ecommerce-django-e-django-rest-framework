from produto.tests.test_base import MyBaseTest

from perfil import views

from django.urls import reverse, resolve


class PerfilLoginViewTest(MyBaseTest):

    def test_perfil_logout_views_function_is_correct(self):
        view = resolve(
            reverse(
                'perfil:logout'
            )
        )
        self.assertIs(view.func.view_class, views.Logout)

    def test_perfil_logout_views_function_returns_status_code_405_if_method_is_post(self):  # noqa: E501
        url = reverse('perfil:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_logout_views_function_returns_status_code_405_if_method_is_patch(self):  # noqa: E501
        url = reverse('perfil:logout')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_logout_views_function_returns_status_code_405_if_method_is_put(self):  # noqa: E501
        url = reverse('perfil:logout')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_logout_views_function_returns_status_code_405_if_method_is_delete(self):  # noqa: E501
        url = reverse('perfil:logout')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_perfil_logout_views_function_returns_status_code_200_if_method_is_get(self):  # noqa: E501
        url = reverse('perfil:logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('produto:lista'))
