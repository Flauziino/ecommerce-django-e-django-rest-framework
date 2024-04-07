from django.test import TestCase
from django.contrib.auth.models import User

from produto.models import Produto, Variacao

from perfil.models import Perfil


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

    def get_auth_data(self):
        user = User.objects.create(
            username='test',
            password='13456'
        )
        return self.client.force_login(user)

    def make_perfil(self):
        user = User.objects.create(
            username='test',
            password='13456'
        )
        user.save()
        self.client.force_login(user)

        return Perfil.objects.create(
            user=user,
            idade=34,
            data_nascimento='1993-03-21',
            cpf='98739945057',
            endereco='Av. Brasil',
            numero='100',
            complemento='A',
            bairro='Centro',
            cep='37410045',
            cidade='Cajuru',
            estado='MG'
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
