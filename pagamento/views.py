import json
import requests

import pytz

from datetime import timedelta, datetime

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from pedido.models import Pedido
from perfil.models import Perfil


def get_public_key():
    url = 'https://sandbox.api.pagseguro.com/public-keys/'
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer E0A4D184FD684D5D9036F8DE1C7DBE34",
        "content-type": "application/json"
    }
    body = json.dumps({
        "type": "card"
    })
    reqs = requests.post(url, headers=headers, data=body)
    return reqs.json()['public_key']


def inicio(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    # Se o parâmetro não estiver presente, o método de pagamento
    # padrão será 'Cartao'
    metodo_pagamento = request.GET.get('metodo_pagamento', 'Cartao')

    data = {
        'public_key': get_public_key(),
        'pedido': pedido,
        'pagamento': metodo_pagamento
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
        # conferindo se o nome do item é menor que 100 chars
        # pois é o limite do pagseguro
        if len(item.produto) > 100:
            nome_produto = item.produto[:99]
        else:
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
    card_holder = request.POST.get('cardHolder')
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
    url = 'https://sandbox.api.pagseguro.com/orders/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer E0A4D184FD684D5D9036F8DE1C7DBE34'
    }
    # corpo de envio para API do pagseguro
    body = json.dumps({
        "reference_id": str(pedido.id),
        "customer": {
            "name": cliente_nome,
            "email": cliente_email,
            "tax_id": cliente_cpf,
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
    # pegando a data de hoje para calcular vencimento do boleto.
    hoje = timezone.now().date()
    vencimento = hoje + timedelta(days=5)
    # pegando o pedido
    pedido = get_object_or_404(Pedido, pk=pk)
    # pegando item pedido
    item_pedido = pedido.itempedido_set.all()

    # como item_pedido sera uma lista
    # é feito um for para passar os valores para dentro de variaveis
    for item in item_pedido:
        # conferindo se o nome do item é menor que 100 chars
        # pois é o limite do pagseguro
        if len(item.produto) > 100:
            nome_produto = item.produto[:99]
        else:
            nome_produto = item.produto

        qtd = item.quantidade
        # checando se tem preço promocional no item
        if item.preco_promocional:
            valor_item = item.preco_promocional
        else:
            valor_item = item.preco

    # pegando o cliente
    cliente = Perfil.objects.get(user=request.user)

    # separando os dados do cliente
    if cliente.user.first_name:
        cliente_nome = cliente.user.first_name
    else:
        cliente_nome = cliente.user.username

    cliente_email = cliente.user.email
    cliente_cpf = cliente.cpf

    # pegando valor total para calcular desconto com boleto.
    valor_total = pedido.total * 100
    # desconto de 10% a vista no boleto.
    disconto_boleto_total = valor_total - (valor_total * 0.1)

    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer E0A4D184FD684D5D9036F8DE1C7DBE34'
    }

    body = json.dumps({
        "reference_id": str(pedido.id),
        "customer": {
            "name": cliente_nome,
            "email": cliente_email,
            "tax_id": cliente_cpf,
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
                "reference_id": str(pedido.id),
                "description": "descricao da cobranca",
                "amount": {
                    "value": int(disconto_boleto_total),
                    "currency": "BRL"
                },
                "payment_method": {
                    "type": "BOLETO",
                    "boleto": {
                        "due_date": str(vencimento),
                        "instruction_lines": {
                            "line_1": "Pagamento processado para DESC Fatura",
                            "line_2": "Via PagSeguro"
                        },
                        "holder": {
                            "name": cliente_nome,
                            "tax_id": cliente_cpf,
                            "email": cliente_email,
                            "address": {
                                "country": "Brasil",
                                "region": cliente.estado,
                                "region_code": cliente.estado,
                                "city": cliente.cidade,
                                "postal_code": cliente.cep,
                                "street": cliente.endereco,
                                "number": cliente.numero,
                                "locality": cliente.bairro
                            }
                        }
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

        link_boleto_pdf = None

        for charge in reqs.json()['charges']:
            if 'links' in charge:
                for link in charge['links']:
                    if link['media'] == 'application/pdf':
                        link_boleto_pdf = link['href']
                        break
                if link_boleto_pdf:
                    break

        # Verificar se o link foi encontrado
        if link_boleto_pdf:
            # Redirecionar para o link do PDF do boleto

            contexto = {
                'ordem_id': ordem_id,
                'pedido': pedido,
                'pagamento': 'BOLETO',
                'link_boleto': link_boleto_pdf
            }

            return render(
                request,
                'pagamento/status_compra.html',
                contexto
            )

    else:
        # Caso ocorra algum problema com o pagamento
        contexto = {
            'erro': 'Não foi possivel gerar o boleto'
        }
        return render(
            request,
            'pagamento/error_pagamento.html',
            contexto
        )


def pix(request, pk):
    # pegando a data de hoje para calcular vencimento do qrcode.
    hoje = datetime.now()

    # Adicionando 5 dias ao momento atual
    vencimento = hoje + timedelta(days=5)

    # Adicionando o fuso horário -03:00
    # -180 minutos é equivalente a -03:00
    fuso_horario = pytz.FixedOffset(-180)
    vencimento_com_fuso = vencimento.astimezone(fuso_horario)

    # Formatando a data e hora no formato ISO-8601
    vencimento_formatado = vencimento_com_fuso.strftime('%Y-%m-%dT%H:%M:%S%z')

    # Inserindo ':' para separar as horas dos minutos no fuso horário
    vencimento_formatado = vencimento_formatado[:-2] + ':' + vencimento_formatado[-2:]  # noqa: E501

    print(vencimento_formatado)
    # pegando o pedido
    pedido = get_object_or_404(Pedido, pk=pk)
    # pegando item pedido
    item_pedido = pedido.itempedido_set.all()

    # como item_pedido sera uma lista
    # é feito um for para passar os valores para dentro de variaveis
    for item in item_pedido:
        # conferindo se o nome do item é menor que 100 chars
        # pois é o limite do pagseguro
        if len(item.produto) > 100:
            nome_produto = item.produto[:99]
        else:
            nome_produto = item.produto

        qtd = item.quantidade
        # checando se tem preço promocional no item
        if item.preco_promocional:
            valor_item = item.preco_promocional
        else:
            valor_item = item.preco

    # pegando o cliente
    cliente = Perfil.objects.get(user=request.user)

    # separando os dados do cliente
    if cliente.user.first_name:
        cliente_nome = cliente.user.first_name
    else:
        cliente_nome = cliente.user.username

    cliente_email = cliente.user.email
    cliente_cpf = cliente.cpf

    # pegando valor total para calcular desconto com boleto.
    valor_total = pedido.total * 100
    # desconto de 10% a vista no boleto.
    disconto_pix_total = valor_total - (valor_total * 0.1)

    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'E0A4D184FD684D5D9036F8DE1C7DBE34'
    }
    body = json.dumps({
        "reference_id": str(pedido.id),
        "customer": {
            "name": cliente_nome,
            "email": cliente_email,
            "tax_id": cliente_cpf,
        },
        "items": [
            {
                "name": nome_produto,
                "quantity": qtd,
                "unit_amount": int(valor_item)
            }
        ],
        "qr_codes": [
            {
                "amount": {
                    "value": int(disconto_pix_total)
                },
                "expiration_date": str(vencimento_formatado),
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
        ]
    })
    reqs = requests.post(url, headers=headers, data=body)
    if reqs.status_code == 201:
        pedido.status = 'Aprovado'
        pedido.save()

        ordem_id = reqs.json()['id']
        qrcode = reqs.json()['qr_codes'][0]['links'][0]['href']

        contexto = {
            'ordem_id': ordem_id,
            'pedido': pedido,
            'pagamento': 'PIX',
            'qrcode': qrcode
        }
        return render(
            request,
            'pagamento/status_compra.html',
            contexto
        )
    else:
        return render(request, 'pagamento/error_pagamento.html')
