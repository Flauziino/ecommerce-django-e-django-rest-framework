from django.urls import reverse, resolve

from pedido import views

from produto.tests.test_base import MyBaseTest
from pedido.models import Pedido, ItemPedido


class PedidoSalvarPedidoViewTest(MyBaseTest):
    def test_produto_salvar_pedido_view_is_correct(self):
        view = resolve(
            reverse(
                'pedido:salvarpedido',
            )
        )
        self.assertIs(view.func.view_class, views.SalvarPedido)

    def test_produto_salvar_pedido_view_redirects_if_not_authenticated_user_status_code_302(self):  # noqa: E501
        url = reverse('pedido:salvarpedido')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_produto_salvar_pedido_view_redirects_if_not_authenticated_user_and_contain_the_error_msg(self):  # noqa: E501
        url = reverse('pedido:salvarpedido')
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Você precisa fazer login.',
            response.content.decode('utf-8')
        )

    def test_produto_salvar_pedido_view_redirects_if_not_authenticated_user_right_url(self):  # noqa: E501
        url = reverse('pedido:salvarpedido')
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, reverse('perfil:criar'))

    def test_produto_salvar_pedido_view_with_authenticated_user(self):
        user = self.get_auth_data()
        url = reverse('pedido:salvarpedido')
        self.client.get(url)

        self.assertTrue(user.is_authenticated)

    def test_produto_salvar_pedido_view_without_carrinho_in_session_redirects(self):  # noqa: E501
        self.get_auth_data()
        url = reverse('pedido:salvarpedido')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_produto_salvar_pedido_view_redirects_if_not_carrinho_in_session_and_contain_the_msg_error(self):  # noqa: E501
        self.get_auth_data()
        url = reverse('pedido:salvarpedido')
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Seu carrinho está vazio.',
            response.content.decode('utf-8')
        )

    def test_produto_salvar_pedido_view_redirects_if_not_carrinho_in_session_right_url(self):  # noqa: E501
        self.get_auth_data()
        url = reverse('pedido:salvarpedido')
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, reverse('produto:lista'))

    def test_produto_salvar_pedido_view_have_carrinho_in_session_redirects_to_pagar_also_uses_correct_template(self):  # noqa: E501
        # pega usuario autenticado
        self.get_auth_data()
        # url que sera usada
        url = reverse('pedido:salvarpedido')
        # criando uma variacao de produto
        variacao = self.make_variacao()

        # definindo alguns valores inicialmente
        # para passar para dentro do dict do carrinho (na session)
        # esses valores precisam ser passados pro dict pois dentro da view
        # eles sao utilizados para calculos
        preco_unitario = variacao.produto.preco_marketing
        preco_unitario_promocional = variacao.produto.preco_marketing_promocional  # noqa: E501

        quantidade = 1

        preco_quantitativo = preco_unitario * quantidade
        preco_quantitativo_promocional = preco_unitario_promocional * quantidade  # noqa: E501

        # pegando a session
        session = self.client.session
        # criando o carrinho linkado a session e passando as variaveis
        # criadas anteriormente
        session['carrinho'] = {
            variacao.id: {
                'produto_id': variacao.produto.id,
                'produto_nome': variacao.produto.nome,
                'variacao_id': variacao.id,
                'variacao_nome': variacao.nome,
                'quantidade': quantidade,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_quantitativo,
                'preco_quantitativo_promocional': preco_quantitativo_promocional,  # noqa: E501
                'imagem': '',
            }
        }
        # salvando a session contendo o carrinho
        session.save()

        # pegando a response do teste
        # para iniciar de fato os testes
        response = self.client.get(url)

        # checando se redirecionou para pg de pagamento
        self.assertRedirects(
            response,
            reverse('pedido:pagar', kwargs={'pk': variacao.id})
        )
        # checando se foi utilizado o template correto
        self.assertTemplateUsed('pedido/pagar.html')

    def test_produto_salvar_pedido_view_have_carrinho_in_session_create_the_right_pedido_and_item_pedido(self):  # noqa: E501
        # pega usuario autenticado
        user = self.get_auth_data()
        # url que sera usada
        url = reverse('pedido:salvarpedido')
        # criando uma variacao de produto
        variacao = self.make_variacao()

        # definindo alguns valores inicialmente
        # para passar para dentro do dict do carrinho (na session)
        # esses valores precisam ser passados pro dict pois dentro da view
        # eles sao utilizados para calculos
        preco_unitario = variacao.produto.preco_marketing
        preco_unitario_promocional = variacao.produto.preco_marketing_promocional  # noqa: E501

        quantidade = 1

        preco_quantitativo = preco_unitario * quantidade
        preco_quantitativo_promocional = preco_unitario_promocional * quantidade  # noqa: E501

        # pegando a session
        session = self.client.session
        # criando o carrinho linkado a session e passando as variaveis
        # criadas anteriormente
        session['carrinho'] = {
            variacao.id: {
                'produto_id': variacao.produto.id,
                'produto_nome': variacao.produto.nome,
                'variacao_id': variacao.id,
                'variacao_nome': variacao.nome,
                'quantidade': quantidade,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_quantitativo,
                'preco_quantitativo_promocional': preco_quantitativo_promocional,  # noqa: E501
                'imagem': '',
            }
        }
        # salvando a session contendo o carrinho
        session.save()

        # pegando a response do teste
        # para iniciar de fato os testes !
        self.client.get(url)

        pedido = Pedido.objects.all()
        item_pedido = ItemPedido.objects.all()

        # checando se o pedido existe
        self.assertTrue(pedido.exists())
        # checando se o item_pedido existe
        self.assertTrue(item_pedido.exists())

        # checando se o pedido é do usuario correto
        self.assertTrue(pedido.first().user, user)

        # por fim checando se o item_pedido esta atrelado corretamente
        # ao pedido criado corretamente
        for item in item_pedido:
            self.assertEqual(item.pedido, pedido.first())

    def test_produto_salvar_pedido_view_have_carrinho_in_session_but_quantidade_gt_estoque(self):  # noqa: E501
        # pega usuario autenticado
        self.get_auth_data()
        # url que sera usada
        url = reverse('pedido:salvarpedido')
        # criando uma variacao de produto
        variacao = self.make_variacao()

        # definindo alguns valores inicialmente
        # para passar para dentro do dict do carrinho (na session)
        # esses valores precisam ser passados pro dict pois dentro da view
        # eles sao utilizados para calculos
        preco_unitario = variacao.produto.preco_marketing
        preco_unitario_promocional = variacao.produto.preco_marketing_promocional  # noqa: E501

        quantidade = 6

        preco_quantitativo = preco_unitario * quantidade
        preco_quantitativo_promocional = preco_unitario_promocional * quantidade  # noqa: E501

        # pegando a session
        session = self.client.session
        # criando o carrinho linkado a session e passando as variaveis
        # criadas anteriormente
        session['carrinho'] = {
            variacao.id: {
                'produto_id': variacao.produto.id,
                'produto_nome': variacao.produto.nome,
                'variacao_id': variacao.id,
                'variacao_nome': variacao.nome,
                'quantidade': quantidade,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_quantitativo,
                'preco_quantitativo_promocional': preco_quantitativo_promocional,  # noqa: E501
                'imagem': '',
            }
        }
        # salvando a session contendo o carrinho
        session.save()

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
