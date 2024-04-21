from pagamento import views

from django.urls import reverse, resolve

from produto.tests.test_base import MyBaseTest
from pedido.models import ItemPedido, Pedido

from unittest.mock import patch, MagicMock


class PagamentoAPIPagseguroPixViewTest(MyBaseTest):
    def test_pagamento_pagseguro_api_pix_view_is_correct(self):
        view = resolve(reverse('pagamento:pix', kwargs={'pk': 1}))
        self.assertIs(view.func, views.pix)

    def test_pagamento_pagseguro_api_pix_view_will_redirect_if_not_auth_user(self):  # noqa: E501
        url = reverse('pagamento:pix', kwargs={'pk': 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_pagamento_pagseguro_api_pix_view_dont_find_produto_return_404_auth_user(self):  # noqa: E501
        # criando pedido (ja vem com auth autenticado)
        pedido = self.make_pedido()
        # simulando id inexistente
        fake_id = pedido.id + 99999

        url = reverse('pagamento:pix', kwargs={'pk': fake_id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_pagamento_pagseguro_api_pix_view_fails_to_create_a_order_and_render_our_error_template(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        url = reverse('pagamento:pix', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_pix_view_item_produto_len_gt_100_chars(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        item_pedido = aux['item_pedido']
        item_pedido.produto = 'A' * 120
        item_pedido.save()

        url = reverse('pagamento:pix', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_pix_view_item_produto_without_preco_promocional(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        url = reverse('pagamento:pix', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_pix_view_item_produto_with_preco_promocional(self):  # noqa: E501
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
            preco_promocional=50,
            quantidade=1,
            imagem=''
        )
        item_pedido.save()

        url = reverse('pagamento:pix', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_pix_view_item_produto_cliente_have_first_name(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        cliente = aux['user']
        cliente.first_name = 'Test'
        cliente.save()

        url = reverse('pagamento:pix', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    @patch('requests.post')
    def test_pix_full_view_test(self, mock_post):
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        # Configurando o objeto de mock para retornar a resposta simulada
        mock_post.return_value = MagicMock(status_code=201)

        # Chamando a view
        url = reverse('pagamento:pix', kwargs={'pk': 1})
        response = self.client.post(url)

        # Testando se o pedido foi atualizado corretamente
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, 'Aprovado')

        # Testando se o template correto foi utilizado
        self.assertTemplateUsed(response, 'pagamento/status_compra.html')

        # Testando se o contexto está correto
        self.assertIn('pagamento', response.context)
        self.assertIn('qrcode_url', response.context)
        self.assertIn('qrcode_text', response.context)
        self.assertEqual(response.context['pagamento'], 'PIX')
