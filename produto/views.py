from django.shortcuts import render  # type:ignore
from django.views.generic import ListView, DetailView  # type:ignore
from django.views import View  # type:ignore
from . import models


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 9


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarCarrinho(ListView):
    ...


class RemoverCarrinho(ListView):
    ...


class Carrinho(View):
    ...


class Finalizar(View):
    ...
