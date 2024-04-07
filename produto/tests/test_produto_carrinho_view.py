from django.urls import reverse, resolve

from produto import views

from .test_base import MyBaseTest


class ProdutoCarrinhoViewTest(MyBaseTest):
    def test_produto_carrinho_view_function_is_correct(self):
        view = resolve(
            reverse('produto:carrinho')
        )
        self.assertIs(view.func.view_class, views.Carrinho)

    def test_produto_carrinho_view_returns_statuscode_200(self):
        url = reverse('produto:carrinho')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_produto_carrinho_view_render_right_template(self):
        url = reverse('produto:carrinho')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'produto/carrinho.html')

    def test_produto_carrinho_view_returns_statuscode_405_if_method_is_post(self):  # noqa: E501
        url = reverse('produto:carrinho')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 405)

    def test_produto_carrinho_view_returns_carrinho_in_context(self):
        url = reverse('produto:carrinho')
        response = self.client.get(url)

        self.assertIn('carrinho', response.context)

    def test_produto_carrinho_view_returns_carrinho_in_context_and_is_empty(self):  # noqa: E501
        url = reverse('produto:carrinho')
        response = self.client.get(url)

        self.assertEqual(response.context['carrinho'], {})

    def test_produto_carrinho_view_returns_carrinho_in_context_and_is_not_empty(self):  # noqa: E501
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'

        self.client.get(url)
        response = self.client.get(url, follow=True)

        # verificando a msg de sucesso
        self.assertIn(
            f'Produto {variacao.produto.nome} {variacao.nome} adicionado ao seu '  # noqa: E501
            'carrinho 2x.',
            response.content.decode('utf-8')
        )

        # url do carrinho com as variacao adicionada
        url_carrinho = reverse('produto:carrinho')
        response = self.client.get(url_carrinho)

        self.assertEqual(
            response.context['carrinho'],
            {'1': {
                'imagem': '',
                'preco_quantitativo': 300.0,
                'preco_quantitativo_promocional': 240.0,
                'preco_unitario': 150.0,
                'preco_unitario_promocional': 120.0,
                'produto_id': 1,
                'produto_nome': 'Camiseta básica TEST',
                'quantidade': 2,
                'slug': 'camiseta-basica-test',
                'variacao_id': '1',
                'variacao_nome': 'tamanho P'
            }}
        )
