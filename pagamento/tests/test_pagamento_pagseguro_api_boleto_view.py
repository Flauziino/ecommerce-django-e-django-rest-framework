from pagamento import views

from django.urls import reverse, resolve

from produto.tests.test_base import MyBaseTest
from pedido.models import ItemPedido, Pedido


from unittest.mock import patch, MagicMock, Mock


class PagamentoAPIPagseguroBoletoViewTest(MyBaseTest):
    def test_pagamento_pagseguro_api_boleto_view_is_correct(self):
        view = resolve(reverse('pagamento:boleto', kwargs={'pk': 1}))
        self.assertIs(view.func, views.boleto)

    def test_pagamento_pagseguro_api_boleto_view_will_redirect_if_not_auth_user(self):  # noqa: E501
        url = reverse('pagamento:boleto', kwargs={'pk': 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_pagamento_pagseguro_api_boleto_view_dont_find_produto_return_404_auth_user(self):  # noqa: E501
        # criando pedido (ja vem com auth autenticado)
        pedido = self.make_pedido()
        # simulando id inexistente
        fake_id = pedido.id + 99999

        url = reverse('pagamento:boleto', kwargs={'pk': fake_id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_pagamento_pagseguro_api_boleto_view_fails_to_create_a_order_and_render_our_error_template(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        url = reverse('pagamento:boleto', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')
        self.assertIn(
            'Não foi possivel gerar o boleto',
            response.context['erro']
        )

    def test_pagamento_pagseguro_api_boleto_view_item_produto_len_gt_100_chars(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        item_pedido = aux['item_pedido']
        item_pedido.produto = 'A' * 120
        item_pedido.save()

        url = reverse('pagamento:boleto', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_boleto_view_item_produto_without_preco_promocional(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        url = reverse('pagamento:boleto', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_boleto_view_item_produto_with_preco_promocional(self):  # noqa: E501
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

        url = reverse('pagamento:boleto', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    def test_pagamento_pagseguro_api_boleto_view_item_produto_cliente_have_first_name(self):  # noqa: E501
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        cliente = aux['user']
        cliente.first_name = 'Test'
        cliente.save()

        url = reverse('pagamento:boleto', kwargs={'pk': pedido.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        # testando se nossa view utilizou a template correta, pois o status
        # code nao foi 201.
        self.assertTemplateUsed(response, 'pagamento/error_pagamento.html')

    @patch('requests.post')
    def test_boleto_full_view_test(self, mock_post):
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        # Criando a resposta simulada da API do PagSeguro com o campo 'charges'
        response_data = {
            "id": "ORDE_E8A44EB1-89BC-4261-9004-739A09B53A8C",
            "reference_id": "ex-00001",
            "created_at": "2023-02-08T15:10:15.763-03:00",
            "customer": {
                "name": "Jose da Silva",
                "email": "email@test.com",
                "tax_id": "12345678909",
                "phones": [
                    {
                        "type": "MOBILE",
                        "country": "55",
                        "area": "11",
                        "number": "999999999"
                    }
                ]
            },
            "items": [
                {
                    "reference_id": "referencia do item",
                    "name": "nome do item",
                    "quantity": 1,
                    "unit_amount": 500
                }
            ],
            "shipping": {
                "address": {
                    "street": "Avenida Brigadeiro Faria Lima",
                    "number": "1384",
                    "complement": "apto 12",
                    "locality": "Pinheiros",
                    "city": "São Paulo",
                    "region_code": "SP",
                    "country": "BRA",
                    "postal_code": "01452002"
                }
            },
            "charges": [
                {
                    "id": "CHAR_BF10AE3B-68D2-430D-AED6-0D5E2C7E180E",
                    "reference_id": "referencia da cobranca",
                    "status": "WAITING",
                    "created_at": "2023-02-08T15:10:15.901-03:00",
                    "description": "descricao da cobranca",
                    "amount": {
                        "value": 500,
                        "currency": "BRL",
                        "summary": {
                            "total": 500,
                            "paid": 0,
                            "refunded": 0
                        }
                    },
                    "payment_response": {
                        "code": "20000",
                        "message": "SUCESSO"
                    },
                    "payment_method": {
                        "type": "BOLETO",
                        "boleto": {
                            "id": "0E243EE1-736A-45EF-B153-CC9B9F0A838F",
                            "barcode": "03399853012970000024227020901016278150000015630",  # noqa: E501
                            "formatted_barcode": "03399.85301 29700.000242 27020.901016 2 78150000015630",  # noqa: E501
                            "due_date": "2023-06-20",
                            "instruction_lines": {
                                "line_1": "Pagamento processado para DESC Fatura",  # noqa: E501
                                "line_2": "Via PagSeguro"
                            },
                            "holder": {
                                "name": "Jose da Silva",
                                "tax_id": "12345679891",
                                "email": "jose@email.com",
                                "address": {
                                    "region": "São Paulo",
                                    "city": "Sao Paulo",
                                    "postal_code": "01452002",
                                    "street": "Avenida Brigadeiro Faria Lima",
                                    "number": "1384",
                                    "locality": "Pinheiros",
                                    "country": "Brasil",
                                    "region_code": "SP"
                                }
                            }
                        }
                    },
                    "links": [
                        {
                            "rel": "SELF",
                            "href": "https://boleto.sandbox.pagseguro.com.br/0e243ee1-736a-45ef-b153-cc9b9f0a838f.pdf",  # noqa: E501
                            "media": "application/pdf",
                            "type": "GET"
                        },
                        {
                            "rel": "SELF",
                            "href": "https://boleto.sandbox.pagseguro.com.br/0e243ee1-736a-45ef-b153-cc9b9f0a838f.png",  # noqa: E501
                            "media": "image/png",
                            "type": "GET"
                        },
                        {
                            "rel": "SELF",
                            "href": "https://sandbox.api.pagseguro.com/charges/CHAR_BF10AE3B-68D2-430D-AED6-0D5E2C7E180E",  # noqa: E501
                            "media": "application/json",
                            "type": "GET"
                        }
                    ]
                }
            ],
            "notification_urls": [
                "https://meusite.com/notificacoes"
            ],
            "links": [
                {
                    "rel": "SELF",
                    "href": "https://sandbox.api.pagseguro.com/orders/ORDE_E8A44EB1-89BC-4261-9004-739A09B53A8C",  # noqa: E501
                    "media": "application/json",
                    "type": "GET"
                },
                {
                    "rel": "PAY",
                    "href": "https://sandbox.api.pagseguro.com/orders/ORDE_E8A44EB1-89BC-4261-9004-739A09B53A8C/pay",  # noqa: E501
                    "media": "application/json",
                    "type": "POST"
                }
            ]
        }

        # Configurando o objeto de mock para retornar a resposta simulada
        mock_post.return_value = MagicMock(
            status_code=201, json=MagicMock(return_value=response_data))

        # Chamando a view
        url = reverse('pagamento:boleto', kwargs={'pk': 1})
        response = self.client.post(url)

        # Testando se o pedido foi atualizado corretamente
        pedido.refresh_from_db()
        self.assertEqual(pedido.status, 'Aprovado')

        # Testando se o template correto foi utilizado
        self.assertTemplateUsed(response, 'pagamento/status_compra.html')

        # Testando se o contexto está correto
        self.assertIn('pagamento', response.context)
        self.assertEqual(response.context['pagamento'], 'BOLETO')

    def test_encontra_link_boleto_pdf(self):
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']

        # Crie um objeto Mock para simular a resposta da requisição
        mock_response = Mock()

        # Defina o status_code e o json() da resposta
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'id': '123',
            'charges': [
                {
                    'links': [
                        {
                            'media': 'application/pdf',
                            'href': 'http://example.com/boleto.pdf'
                        },
                        # Adicione mais links se necessário
                    ]
                },
                # Adicione mais charges se necessário
            ]
        }

        url = reverse('pagamento:boleto', kwargs={'pk': pedido.id})
        # Substitua a função requests.post pelo seu mock
        with patch('requests.post', return_value=mock_response):
            # Chame a função boleto
            self.client.post(url)
            link_boleto_pdf = 'http://example.com/boleto.pdf'
            charges_processed = 1
            # Verifique se o link do boleto foi encontrado
            self.assertEqual(
                link_boleto_pdf,
                'http://example.com/boleto.pdf')

            # Verifique se o loop percorreu todos os 'charges'
            self.assertEqual(len(
                mock_response.json.return_value['charges']),
                charges_processed)

    @patch('requests.get')
    def test_sem_link_boleto_pdf(self, mock_get):
        aux = self.get_aux_pag_seguro_test()
        pedido = aux['pedido']
        # Suponha que `reqs.json()['charges']` seja uma lista de cobranças
        reqs = MagicMock()
        reqs.json.return_value = {
            "charges": [
                {"links": []},
                {"links": []}
            ]
        }

        mock_get.return_value = reqs

        # Chamando a view que não deve encontrar nenhum link do boleto PDF
        url = reverse('pagamento:boleto', kwargs={'pk': pedido.id})
        response = self.client.get(url)

        # Teste se nenhum link do PDF foi encontrado
        self.assertEqual(response.status_code, 200)


# TODO #####
