from django.shortcuts import render  # type:ignore
from django.views.generic.list import ListView  # type:ignore
from django.views import View  # type:ignore
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'


class DetalheProduto(View):
    ...


class AdicionarCarrinho(ListView):
    ...


class RemoverCarrinho(ListView):
    ...


class Carrinho(View):
    ...


class Finalizar(View):
    ...
