from django.urls import path  # type:ignore
from . import views


app_name = 'pedido'

urlpatterns = [
    path(
        'pagar/',
        views.Pagar.as_view(),
        name='pagar'
    ),

    path(
        'fecharpedido/',
        views.FecharPedido.as_view(),
        name='fecharpedido'
    ),

    path(
        'detalhe/',
        views.Detalhe.as_view(),
        name='detalhe'
    ),
]
