from django.urls import path  # type:ignore

from pagamento import views


app_name = 'pagamento'

urlpatterns = [
    path('inicio/<int:pk>', views.inicio, name='inicio'),
    path(
        'controle-pagamento/<int:pk>/credito',
        views.cartao_cred,
        name='credito'
    ),
    path(
        'controle-pagamento/<int:pk>/boleto',
        views.boleto,
        name='boleto'
    ),
    path(
        'controle-pagamento/<int:pk>/pix',
        views.pix,
        name='pix'
    ),
]
