from django.conf import settings
from django.core.exceptions import ValidationError

import os

from PIL import Image

from parameterized import parameterized

from produto.models import Produto
from .test_base import MyBaseTest


class ProdutoModelsTest(MyBaseTest):
    def setUp(self) -> None:
        # criando uma imagem fake
        self.image_django = 'test_image.jpg'
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.image_django)
        # Resolvendo o caminho absoluto se necessário
        self.image_path = os.path.abspath(self.image_path)
        self.image = Image.new('RGB', (800, 600), 'white')
        self.image.save(self.image_path, 'JPEG')

    # Model PRODUTO
    @parameterized.expand([
        ('nome', 270),
        ('tipo', 2),
    ])
    def test_produto_produto_model_max_length(self, field, max_length):
        produto = self.make_produto()
        setattr(produto, field, 'S' * max_length)

        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_produto_string_representation(self):
        produto = self.make_produto()
        produto.nome = 'Testing representation'
        produto.full_clean()
        produto.save()
        self.assertEqual(
            str(produto), 'Testing representation'
        )

    def test_produto_preco_marketing_promocional_is_0_by_default(self):
        produto = self.make_produto_no_defaults()
        self.assertEqual(
            produto.preco_marketing_promocional, 0
        )

    def test_produto_tipo_is_V_by_default(self):
        produto = self.make_produto_no_defaults()
        self.assertEqual(
            produto.tipo, 'V'
        )

    def test_produto_get_preco_marketing_formatado_method_is_correct(self):
        produto = self.make_produto()
        produto.preco_marketing = 500

        self.assertEqual(
            produto.get_preco_marketing_formatado(), 'R$ 500,00'
        )

    def test_produto_get_preco_marketing_promocional_formatado_method_is_correct(self):  # noqa: E501
        produto = self.make_produto()
        produto.preco_marketing_promocional = 300

        self.assertEqual(
            produto.get_preco_marketing_promocional_formatado(), 'R$ 300,00'
        )

    def test_produto_save_method_is_correct_looking_for_slug(self):
        produto = self.make_produto()

        self.assertEqual(produto.slug, 'camiseta-basica-test')

    def test_produto_resize_imagem_method_is_working_right(self):
        # Criando uma instância de Quarto
        produto = self.make_produto()

        # adicionando uma imagem
        produto.imagem = self.image_django
        produto.save()

        # Carregando a imagem usando o caminho
        image_obj = Image.open(self.image_path)

        # Chamando o método resize_image() com o objeto de imagem
        produto.resize_image(image_obj, new_width=400)

        # Verificando se a nova imagem foi salva corretamente
        self.assertTrue(os.path.exists(self.image_path))

        # Carregando a nova imagem para verificar suas dimensões
        new_image = Image.open(self.image_path)

        # Verificando se a nova imagem tem o mesmo tamanho que
        # foi passado para dentro da função
        self.assertEqual(new_image.size, (400, 300))

    # Model VARIACAO
    def test_variacao_string_representation_by_variacao(self):
        variacao = self.make_variacao()
        variacao.nome = 'Testing representation'
        variacao.full_clean()
        variacao.save()
        self.assertEqual(
            str(variacao), 'Testing representation'
        )

    def test_variacao_string_representation_by_produto(self):
        variacao = self.make_variacao()
        variacao.full_clean()
        variacao.save()
        self.assertEqual(
            str(variacao.produto), 'Camiseta básica TEST'
        )

    def test_variacao_nome_field_max_length(self):
        variacao = self.make_variacao()
        variacao.nome = 'A' * 300

        with self.assertRaises(ValidationError):
            variacao.full_clean()

    def test_variacao_produto_field_is_instance_of_produto_model(self):
        variacao = self.make_variacao()
        self.assertIsInstance(variacao.produto, Produto)

    def test_variacao_get_preco_formatado_method_is_correct(self):
        variacao = self.make_variacao()
        self.assertEqual(variacao.get_preco_formatado(), 'R$ 150,00')

    def test_variacao_get_preco_promocional_formatado_method_is_correct(self):
        variacao = self.make_variacao()
        self.assertEqual(
            variacao.get_preco_promocional_formatado(), 'R$ 120,00'
        )

    def test_variacao_preco_promocional_is_0_by_default(self):
        variacao = self.make_variacao_no_defaults()
        self.assertEqual(
            variacao.preco_promocional, 0
        )

    def test_estoque_is_1_by_default(self):
        variacao = self.make_variacao_no_defaults()
        self.assertEqual(
            variacao.estoque, 1
        )
