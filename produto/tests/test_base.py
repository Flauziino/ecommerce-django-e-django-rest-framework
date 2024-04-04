from django.test import TestCase

from produto.models import Produto, Variacao


class MyBaseTest(TestCase):

    def make_produto(self):
        return Produto.objects.create(
            nome='Camiseta básica TEST',
            descricao_curta='test test',
            descricao_longa='um longo test',
            slug='',
            preco_marketing=1500,
            preco_marketing_promocional=1300,
            tipo='S'
        )

    def make_produto_no_defaults(self):
        return Produto.objects.create(
            nome='Camiseta básica TEST',
            descricao_curta='test test',
            descricao_longa='um longo test',
            slug='',
            preco_marketing=1500,
        )

    def make_variacao(self):
        produto = self.make_produto()
        return Variacao.objects.create(
            nome='tamanho P',
            produto=produto,
            preco=150,
            preco_promocional=120,
            estoque=5
        )

    def make_variacao_no_defaults(self):
        produto = self.make_produto()
        return Variacao.objects.create(
            nome='tamanho P',
            produto=produto,
            preco=150,
        )
