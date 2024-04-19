from pagamento import views

from django.urls import reverse, resolve

from produto.tests.test_base import MyBaseTest
from pedido.models import Pedido, ItemPedido

from unittest.mock import patch
import json


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data
        self.text = json.dumps(json_data)

    def json(self):
        return self.json_data


def mock_post(*args, **kwargs):
    return MockResponse(201, {'id': 'mock_order_id'})


class PagamentoAPIPagseguroCartaoCreditoViewTest(MyBaseTest):
    def test_pagamento_pagseguro_api_cartao_credito_view_is_correct(self):
        view = resolve(reverse('pagamento:credito', kwargs={'pk': 1}))
        self.assertIs(view.func, views.cartao_cred)

    def test_pagamento_pagseguro_api_cartao_credito_view_will_redirect_if_not_auth_user(self):  # noqa: E501
        url = reverse('pagamento:credito', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_pagamento_pagseguro_api_cartao_credito_view_dont_find_produto_return_404_auth_user(self):  # noqa: E501
        # criando pedido (ja vem com auth autenticado)
        pedido = self.make_pedido()
        # simulando id inexistente
        fake_id = pedido.id + 99999

        url = reverse('pagamento:credito', kwargs={'pk': fake_id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_pagamento_pagseguro_api_cartao_credito_view_fails_to_create_a_order_and_render_our_error_template(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        url = reverse('pagamento:credito', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_cartao_credito_view_item_produto_len_gt_100_chars(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        item_pedido = aux['item_pedido']
        item_pedido.produto = 'A' * 120
        item_pedido.save()

        url = reverse('pagamento:credito', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_cartao_credito_view_item_produto_without_preco_promocional(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        url = reverse('pagamento:credito', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_cartao_credito_view_item_produto_with_preco_promocional(self):  # noqa: E501
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

        url = reverse('pagamento:credito', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_cartao_credito_view_item_produto_cliente_have_first_name(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        cliente = aux['user']
        cliente.first_name = 'Test'
        cliente.save()

        url = reverse('pagamento:credito', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    @patch('requests.post', side_effect=mock_post)
    def test_cartao_cred_full_view_test(self, mock_post):
        # chamando o auxiliar para pegar o pedido
        aux = self.get_aux_pag_seguro_test()
        # pegando pedido para passar o id para url
        pedido = aux['pedido']

        url = reverse('pagamento:credito', kwargs={'pk': pedido.id})
        # pegando a response passando os dados como se fosse um usuario
        # digitando o cartao no frontend
        response = self.client.post(url, {
            'cardHolder': 'Test User',
            'cardCvv': '123',
            'encriptedCard': 'encryptedCardTest'
        })
        self.assertEqual(response.status_code, 200)
        # atualizando o pedido da base de dados.
        pedido.refresh_from_db()
        # verificando se o pedido atualizou para aprovado
        self.assertEqual(pedido.status, 'Aprovado')
        # verificando se esta utilizando o template correto
        self.assertTemplateUsed(response, 'pagamento/status_compra.html')
        # verificando contexto
        self.assertIn('pagamento', response.context)
        # verificando se o context PAGAMENTO esta como CREDIT_CARD
        self.assertEqual(response.context['pagamento'], 'CREDIT_CARD')
