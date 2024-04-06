from django.urls import reverse, resolve

from produto import views

from .test_base import MyBaseTest


class ProdutoRemoverCarrinhoViewTest(MyBaseTest):
    def test_remover_carrinho_view_function_is_correct(self):
        view = resolve(
            reverse('produto:removercarrinho')
        )
        self.assertIs(view.func.view_class, views.RemoverCarrinho)

    def test_produto_remover_carrinho_view_returns_statuscode_302_if_not_HTTP_REFERER_and_redirect_to_produto_lista(self):  # noqa: E501
        url = reverse('produto:removercarrinho')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_produto_remover_carrinho_view_got_variacao_id(self):
        variacao = self.make_variacao()
        url = reverse('produto:removercarrinho') + f'?vid={variacao.id}'
        self.client.get(url)

        self.assertEqual(variacao.id, 1)

    def test_produto_remover_carrinho_view_got_variacao_id_but_dont_have_carrinho_and_redirects(self):  # noqa: E501
        variacao = self.make_variacao()
        url = reverse('produto:removercarrinho') + f'?vid={variacao.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_produto_remover_carrinho_view_got_variacao_and_already_have_a_carrinho(self):  # noqa: E501
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:removercarrinho') + f'?vid={variacao.id}'

        # pegando a session
        session = self.client.session
        # criando o carrinho linkado a session
        session['carrinho'] = {'test': '1'}
        # salvando o carrinho
        session.save()

        self.client.get(url)
        self.assertIn('carrinho', session)

    def test_produto_remover_carrinho_view_got_variacao_id_and_variacao_id_is_not_in_carrinho_so_redirect(self):  # noqa: E501
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:removercarrinho') + f'?vid={variacao.id}'

        response = self.client.get(url)

        self.assertNotIn('carrinho', self.client.session)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_produto_remover_carrinho_view_got_variacao_id_and_variacao_id_is_in_carrinho_so_we_remove_variacao_id_from_carrinho(self):  # noqa: E501
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:removercarrinho') + f'?vid={variacao.id}'

        # pegando a session
        session = self.client.session
        # criando o carrinho linkado a session
        session['carrinho'] = {
            variacao.id: {
                'produto_nome': variacao.produto.nome,
                'variacao_nome': variacao.nome
            }
        }
        # salvando o carrinho
        session.save()

        response = self.client.get(url, follow=True)
        carrinho = session['carrinho'][variacao.id]

        self.assertIn('carrinho', self.client.session)
        # verificando se a variacao_id não esta mais no carrinho
        # concluindo assim a remoção
        self.assertNotIn(
            str(variacao.id),
            self.client.session['carrinho']
        )
        # verificando se a msg de sucesso da remoção esta na resposta.
        self.assertIn(
            f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"]} '
            f'removido do seu carrinho.',
            response.content.decode('utf-8')
        )
        # verificando se foi feito o redirecionamento
        self.assertRedirects(response, '/')
