from django.contrib import admin  # type:ignore
from django.urls import path, include  # type:ignore
from django.conf import settings  # type:ignore
from django.conf.urls.static import static  # type:ignore


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produto.urls')),
    path('perfil/', include('perfil.urls')),
    path('pedido/', include('pedido.urls')),
    path('pagar/', include('pagamento.urls'))
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
