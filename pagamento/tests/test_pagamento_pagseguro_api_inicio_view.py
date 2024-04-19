from django.urls import reverse, resolve

from pagamento import views

from produto.tests.test_base import MyBaseTest


# Com esses testes, a funcao get_public_key sera testada tb por agregação
class PagamentoAPIPagseguroInicioViewTest(MyBaseTest):
    def test_pagamento_pagseguro_api_inicio_view_is_correct(self):
        view = resolve(reverse('pagamento:inicio', kwargs={'pk': 1}))
        self.assertIs(view.func, views.inicio)

    def test_pagamento_pagseguro_api_inicio_view_dont_find_produto_return_404_auth_user(self):  # noqa: E501
        # criando pedido (ja vem com auth autenticado)
        pedido = self.make_pedido()
        # simulando id inexistente
        fake_id = pedido.id + 99999

        url = reverse('pagamento:inicio', kwargs={'pk': fake_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_pagamento_pagseguro_api_inicio_view_find_pedido_auth_user(self):
        # criando pedido (ja vem com auth autenticado)
        pedido = self.make_pedido()
        # simulando id inexistente

        url = reverse('pagamento:inicio', kwargs={'pk': pedido.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_pagamento_pagseguro_api_inicio_view_will_redirect_if_not_auth_user(self):  # noqa: E501
        url = reverse('pagamento:inicio', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_pagamento_pagseguro_api_inicio_view_will_use_right_template(self):
        pedido = self.make_pedido()
        url = reverse('pagamento:inicio', kwargs={'pk': pedido.id})
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'pagamento/pagamento.html')

    def test_pagamento_pagseguro_api_inicio_view_have_right_context(self):
        pedido = self.make_pedido()
        url = reverse('pagamento:inicio', kwargs={'pk': pedido.id})
        response = self.client.get(url)

        # procurando a publickey
        self.assertIn('public_key', response.context)
        # procurando o pedido
        self.assertIn('pedido', response.context)
        # procurando o pagamento
        self.assertIn('pagamento', response.context)

    def test_pagamento_pagseguro_api_inicio_view_pagamento_is_Cartao_by_default(self):  # noqa: E501
        pedido = self.make_pedido()
        url = reverse('pagamento:inicio', kwargs={'pk': pedido.id})
        response = self.client.get(url)

        self.assertEqual(response.context['pagamento'], 'Cartao')

    def test_pagamento_pagseguro_api_inicio_view_public_key_is_right(self):
        pedido = self.make_pedido()
        url = reverse('pagamento:inicio', kwargs={'pk': pedido.id})
        response = self.client.get(url)

        public_key = views.get_public_key()

        self.assertEqual(response.context['public_key'], public_key)
