from django.test import TestCase
from django.urls import reverse


class PerfilURLsTest(TestCase):
    def test_perfil_criar_url_is_correct(self):
        url = reverse('perfil:criar')
        self.assertEqual(url, '/perfil/')

    def test_perfil_atualizar_url_is_correct(self):
        url = reverse('perfil:atualizar')
        self.assertEqual(url, '/perfil/atualizar/')

    def test_perfil_login_url_is_correct(self):
        url = reverse('perfil:login')
        self.assertEqual(url, '/perfil/login/')

    def test_perfil_logout_url_is_correct(self):
        url = reverse('perfil:logout')
        self.assertEqual(url, '/perfil/logout/')
