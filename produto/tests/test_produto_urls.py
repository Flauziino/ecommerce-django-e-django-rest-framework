from django.test import TestCase
from django.urls import reverse


class ProdutoURLsTest(TestCase):
    def test_produto_index_url_is_correct(self):
        url = reverse('produto:lista')
        self.assertEqual(url, '/')

    def test_produto_slug_url_is_correct(self):
        url = reverse('produto:detalhe', kwargs={'slug': 'X3tx'})
        self.assertEqual(url, '/X3tx')

    def test_produto_adicionar_carrinho_url_is_correct(self):
        url = reverse('produto:adicionarcarrinho')
        self.assertEqual(url, '/adicionarcarrinho/')

    def test_produto_remover_carrinho_url_is_correct(self):
        url = reverse('produto:removercarrinho')
        self.assertEqual(url, '/removercarrinho/')

    def test_produto_carrinho_url_is_correct(self):
        url = reverse('produto:carrinho')
        self.assertEqual(url, '/carrinho/')

    def test_produto_resumo_da_compra_url_is_correct(self):
        url = reverse('produto:resumodacompra')
        self.assertEqual(url, '/resumodacompra/')

    def test_produto_busca_url_is_correct(self):
        url = reverse('produto:busca')
        self.assertEqual(url, '/busca/')
