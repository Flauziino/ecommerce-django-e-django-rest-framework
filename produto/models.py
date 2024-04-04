import os
from django.db import models  # type:ignore
from PIL import Image   # type:ignore
from django.conf import settings   # type:ignore
from django.utils.text import slugify  # type:ignore


class Produto(models.Model):
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField()
    descricao_longa = models.TextField()

    imagem = models.ImageField(
        upload_to='produto_img/%Y/%m',
        blank=True,
        null=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    preco_marketing = models.FloatField(verbose_name='Preço')

    preco_marketing_promocional = models.FloatField(
        default=0,
        verbose_name='Preço promocional'
    )

    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_preco_marketing_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.', ',')
    get_preco_marketing_formatado.short_description = 'Preço'

    def get_preco_marketing_promocional_formatado(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.', ',')
    preco_promo = 'Preço promocional'
    get_preco_marketing_promocional_formatado.short_description = preco_promo

    @staticmethod
    def resize_image(img, new_width=800):
        if isinstance(img, Image.Image):
            img_full_path = os.path.join(
                settings.MEDIA_ROOT,
                img.filename
            )
        else:
            img_full_path = os.path.join(
                settings.MEDIA_ROOT,
                img.name
            )

        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round(
            (new_width * original_height) / original_width
        )

        new_img = img_pil.resize(
            (new_width, new_height), Image.LANCZOS
        )

        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_img_size = 800
        if self.imagem:
            self.resize_image(self.imagem, max_img_size)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    nome = models.CharField(max_length=255, blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def get_preco_formatado(self):
        return f'R$ {self.preco:.2f}'.replace('.', ',')

    def get_preco_promocional_formatado(self):
        return f'R$ {self.preco_promocional:.2f}'.replace('.', ',')

    def __str__(self):
        return self.nome or self.produto.nome
