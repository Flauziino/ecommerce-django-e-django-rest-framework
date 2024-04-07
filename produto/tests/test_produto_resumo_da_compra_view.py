from django.urls import reverse, resolve

from produto import views

from .test_base import MyBaseTest


class ProdutoResumoDaCompraViewTest(MyBaseTest):
    def test_produto_resumo_da_compra_view_function_is_correct(self):
        view = resolve(
            reverse('produto:resumodacompra')
        )
        self.assertIs(view.func.view_class, views.ResumoDaCompra)

    def test_produto_resumo_da_compra_view_returns_statuscode_302_if_not_authenticated(self):  # noqa: E501
        url = reverse('produto:resumodacompra')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_produto_resumo_da_compra_view_returns_statuscode_405_if_method_is_post(self):  # noqa: E501
        url = reverse('produto:resumodacompra')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 405)

    def test_produto_resumo_da_compra_view_returns_statuscode_got_user_but_not_perfil(self):  # noqa: E501
        self.get_auth_data()
        url = reverse('produto:resumodacompra')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Usuário sem perfil.',
            response.content.decode('utf-8')
        )

    def test_produto_resumo_da_compra_view_returns_statuscode_got_user_and_user_have_perfil_but_carrinho_vazio(self):  # noqa: E501
        self.make_perfil()

        url = reverse('produto:resumodacompra')
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Carrinho vazio.',
            response.content.decode('utf-8')
        )

    def test_produto_resumo_da_compra_view_returns_statuscode_got_user_and_user_have_perfil_and_have_carrinho(self):  # noqa: E501
        # fazendo um perfil
        # pela configuraçao o perfil ja vem com um usuario logado.
        self.make_perfil()

        # pegando a url do resumo da compra que sera usado mais tarde
        url_resumo = reverse('produto:resumodacompra')
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'
        # adicionando dois items no carrinho
        self.client.get(url)
        response = self.client.get(url, follow=True)

        # verificando a msg de sucesso
        self.assertIn(
            f'Produto {variacao.produto.nome} {variacao.nome} adicionado ao seu '  # noqa: E501
            'carrinho 2x.',
            response.content.decode('utf-8')
        )

        # pegando a response da url do resumo da compra
        # que foi pega anteriormente
        response = self.client.get(url_resumo)

        # conferindo se o status eh 200
        self.assertEqual(response.status_code, 200)
        # conferindo se usuario e carrinho estao no contexto
        self.assertIn('usuario', response.context)
        self.assertIn('carrinho', response.context)
        # conferindo se o template usado foi o correto
        self.assertTemplateUsed(response, 'produto/resumodacompra.html')
