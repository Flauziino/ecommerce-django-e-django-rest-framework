from django.test import TestCase
from django.contrib.auth.models import User

from produto.models import Produto, Variacao

from perfil.models import Perfil
# from perfil.forms import PerfilForm, UserForm
from pedido.models import Pedido, ItemPedido


class MyBaseTest(TestCase):

    def get_auth_data(self):
        user = User.objects.create_user(
            username='test',
            password='13456'
        )
        self.client.force_login(user)
        return user

    def make_perfil(self):
        return Perfil.objects.create(
            user=self.get_auth_data(),
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

    def make_pedido(self):
        return Pedido.objects.create(
            user=self.get_auth_data(),
            total=150.55,
            qtd_total=2
        )

    def make_item_pedido(self):
        pedido = self.make_pedido()
        return ItemPedido.objects.create(
            pedido=pedido,
            produto='camiseta basica',
            produto_id='1',
            variacao='tamanho P',
            variacao_id='1',
            preco=75,
            preco_promocional=70,
            quantidade=1,
            imagem=''
        )

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

    def make_variacao(self):
        produto = self.make_produto()
        return Variacao.objects.create(
            nome='tamanho P',
            produto=produto,
            preco=150,
            preco_promocional=120,
            estoque=5
        )

    def make_produto_no_defaults(self):
        return Produto.objects.create(
            nome='Camiseta básica TEST',
            descricao_curta='test test',
            descricao_longa='um longo test',
            slug='',
            preco_marketing=1500,
        )

    def make_variacao_no_defaults(self):
        produto = self.make_produto()
        return Variacao.objects.create(
            nome='tamanho P',
            produto=produto,
            preco=150,
        )

    def make_item_pedido_no_defaults(self):
        pedido = self.make_pedido()
        return ItemPedido.objects.create(
            pedido=pedido,
            produto='camiseta basica',
            produto_id='1',
            variacao='tamanho P',
            variacao_id='1',
            preco=75,
            quantidade=1,
            imagem=''
        )

    def get_aux_pag_seguro_test(self):
        # criando perfil
        perfil = self.make_perfil()
        # pegando uma instancia de user direto de perfil
        user = perfil.user
        user.save()
        # criando pedido
        pedido = Pedido.objects.create(
            user=user,
            total=150.55,
            qtd_total=2
        )
        pedido.save()
        # criando item_pedido
        item_pedido = ItemPedido.objects.create(
            pedido=pedido,
            produto='camiseta basica',
            produto_id='1',
            variacao='tamanho P',
            variacao_id='1',
            preco=75,
            quantidade=1,
            imagem=''
        )
        item_pedido.save()

        return {
            'perfil': perfil,
            'user': user,
            'pedido': pedido,
            'item_pedido': item_pedido
        }
