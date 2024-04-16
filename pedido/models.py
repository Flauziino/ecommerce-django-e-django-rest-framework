from django.db import models  # type:ignore
from django.contrib.auth.models import User  # type:ignore


class Pedido(models.Model):
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    STATUS_CHOICES = (
        ('A', 'Aprovado'), ('C', 'Criado'),
        ('R', 'Reprovado'), ('P', 'Pendente'),
        ('E', 'Enviado'), ('F', 'Finalizado'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return f'Pedido N. {self.id}'


class ItemPedido(models.Model):
    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'
