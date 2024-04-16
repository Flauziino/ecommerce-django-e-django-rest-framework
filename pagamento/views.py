import json
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from pedido.models import Pedido
from perfil.models import Perfil


def get_public_key():
    url = 'https://sandbox.api.pagseguro.com/public-keys/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'E0A4D184FD684D5D9036F8DE1C7DBE34'
    }
    body = json.dumps({
        "type": "card"
    })
    reqs = requests.post(url, headers=headers, data=body)
    return reqs.json()['public_key']


def inicio(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    data = {
        'public_key': get_public_key(),
        'pedido': pedido
    }
    return render(
        request,
        'pagamento/pagamento.html',
        data
    )


def cartao_cred(request, pk):
    # pegando o pedido
    pedido = get_object_or_404(Pedido, pk=pk)
    # pegando item pedido
    item_pedido = pedido.itempedido_set.all()

    # como item_pedido sera uma lista
    # é feito um for para passar os valores para dentro de variaveis
    for item in item_pedido:
        nome_produto = item.produto
        qtd = item.quantidade
        # checando se tem preço promocional no item
        if item.preco_promocional:
            valor_item = item.preco_promocional
        else:
            valor_item = item.preco

    # pegando o cliente
    cliente = Perfil.objects.get(user=request.user)

    # Aqui obtem os dados do formulário do request.POST
    # do cartão de credito
    card_number = request.POST.get('cardNumber')
    card_holder = request.POST.get('cardHolder')
    card_month = request.POST.get('cardMonth')
    card_year = request.POST.get('cardYear')
    card_cvv = request.POST.get('cardCvv')
    encrypted_card = request.POST.get('encriptedCard')

    # separando os dados do cliente
    if cliente.user.first_name:
        cliente_nome = cliente.user.first_name
    else:
        cliente_nome = cliente.user.username

    cliente_email = cliente.user.email
    cliente_cpf = cliente.cpf

    # iniciando a integração com a API do pagseguro
    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'E0A4D184FD684D5D9036F8DE1C7DBE34'
    }
    # corpo de envio para API do pagseguro
    body = json.dumps({
        "reference_id": str(pedido.id),
        "customer": {
            "name": cliente_nome,
            "email": cliente_email,
            "tax_id": cliente_cpf,
            "phones": [
                {
                    "country": "55",
                    "area": "11",
                    "number": "999999999",
                    "type": "MOBILE"
                }
            ]
        },
        "items": [
            {
                "reference_id": str(pedido.id),
                "name": nome_produto,
                "quantity": qtd,
                "unit_amount": int(valor_item * 100)
            }
        ],
        "shipping": {
            "address": {
                "street": cliente.endereco,
                "number": cliente.numero,
                "complement": cliente.complemento,
                "locality": cliente.bairro,
                "city": cliente.cidade,
                "region_code": cliente.estado,
                "country": "BRA",
                "postal_code": cliente.cep
            }
        },
        "notification_urls": [
            "https://meusite.com/notificacoes"
        ],
        "charges": [
            {
                "reference_id": f"Pedido {str(pedido.id)}",
                "description": "descricao da cobranca",
                "amount": {
                    "value": int(pedido.total * 100),
                    "currency": "BRL"
                },
                "payment_method": {
                    'soft_descriptor': 'Just a E-Commerce',
                    "type": "CREDIT_CARD",
                    "installments": 1,
                    "capture": True,
                    "card": {
                        "encrypted": encrypted_card,
                        "security_code": card_cvv,
                        "holder": {
                            "name": card_holder
                        },
                        "store": True
                    }
                }
            }
        ]
    })
    reqs = requests.post(url, headers=headers, data=body)
    if reqs.status_code == 201:
        pedido.status = 'Aprovado'
        pedido.save()

        ordem_id = reqs.json()['id']
        contexto = {
            'ordem_id': ordem_id,
            'pedido': pedido,
            'pagamento': 'CREDIT_CARD'
        }
        return render(
            request,
            'pagamento/status_compra.html',
            contexto
        )
    else:
        return render(request, 'pagamento/error_pagamento.html')


def boleto(request, pk):
    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'E0A4D184FD684D5D9036F8DE1C7DBE34'
    }
    body = json.dumps({
        "reference_id": "ex-00001",
        "customer": {
            "name": "Jose da Silva",
            "email": "email@test.com",
            "tax_id": "12345679891",
            "phones": [
                {
                    "country": "55",
                    "area": "11",
                    "number": "999999999",
                    "type": "MOBILE"
                }
            ]
        },
        "items": [
            {
                "reference_id": "referencia do item",
                "name": "nome do item",
                "quantity": 1,
                "unit_amount": 5000
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
        "notification_urls": [
            "https://meusite.com/notificacoes"
        ],
        "charges": [
            {
                "reference_id": "referencia da cobranca",
                "description": "descricao da cobranca",
                "amount": {
                    "value": 500,
                    "currency": "BRL"
                },
                "payment_method": {
                    "type": "BOLETO",
                    "boleto": {
                        "due_date": "2024-04-18",
                        "instruction_lines": {
                            "line_1": "Pagamento processado para DESC Fatura",
                            "line_2": "Via PagSeguro"
                        },
                        "holder": {
                            "name": "Jose da Silva",
                            "tax_id": "12345679891",
                            "email": "jose@email.com",
                            "address": {
                                "country": "Brasil",
                                "region": "São Paulo",
                                "region_code": "SP",
                                "city": "Sao Paulo",
                                "postal_code": "01452002",
                                "street": "Avenida Brigadeiro Faria Lima",
                                "number": "1384",
                                "locality": "Pinheiros"
                            }
                        }
                    }
                }
            }
        ]
    })
    reqs = requests.post(url, headers=headers, data=body)
    return HttpResponse(reqs)
    return redirect(reqs.json()['links'][0]['href'])  # verificar depois


def pix(request, pk):
    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'E0A4D184FD684D5D9036F8DE1C7DBE34'
    }
    body = json.dumps({
        "reference_id": "ex-00001",
        "customer": {
            "name": "Jose da Silva",
            "email": "email@test.com",
            "tax_id": "12345678909",
            "phones": [
                {
                    "country": "55",
                    "area": "11",
                    "number": "999999999",
                    "type": "MOBILE"
                }
            ]
        },
        "items": [
            {
                "name": "nome do item",
                "quantity": 1,
                "unit_amount": 500
            }
        ],
        "qr_codes": [
            {
                "amount": {
                    "value": 500
                },
                "expiration_date": "2024-07-29T20:15:59-03:00",
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
        "notification_urls": [
            "https://meusite.com/notificacoes"
        ]
    })
    reqs = requests.post(url, headers=headers, data=body)
    return redirect(reqs.json()['qr_codes'][0]['links'][0]['href'])
