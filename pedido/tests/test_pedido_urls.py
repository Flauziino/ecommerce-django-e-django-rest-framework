from django.test import TestCase
from django.urls import reverse


class PedidoURLsTest(TestCase):
    def test_produto_pagar_url_is_correct(self):
        url = reverse('pedido:pagar', kwargs={'pk': 1})
        self.assertEqual(url, '/pedido/pagar/1')

    def test_produto_salvarpedido_url_is_correct(self):
        url = reverse('pedido:salvarpedido')
        self.assertEqual(url, '/pedido/salvarpedido/')

    def test_produto_lista_url_is_correct(self):
        url = reverse('pedido:lista')
        self.assertEqual(url, '/pedido/lista/')

    def test_produto_detalhe_url_is_correct(self):
        url = reverse('pedido:detalhe', kwargs={'pk': 1})
        self.assertEqual(url, '/pedido/detalhe/1')
