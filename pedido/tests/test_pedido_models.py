from django.core.exceptions import ValidationError

from parameterized import parameterized

from produto.tests.test_base import MyBaseTest


class PedidoModelsTest(MyBaseTest):
    # TEST do Model Pedido
    def test_pedido_model_string_representation(self):
        pedido = self.make_pedido()
        self.assertEqual(str(pedido), f'Pedido N. {pedido.id}')

    def test_pedido_model_status_is_C_by_default(self):
        pedido = self.make_pedido()
        self.assertEqual(
            pedido.status, 'C'
        )

    # TEST do Model ItemPedido
    def test_item_pedido_model_string_representation(self):
        item_pedido = self.make_item_pedido()
        self.assertEqual(str(item_pedido), f'Item do {item_pedido.pedido}')

    def test_item_pedido_model_preco_promocional_is_0_by_default(self):
        item_pedido = self.make_item_pedido_no_defaults()
        self.assertEqual(item_pedido.preco_promocional, 0)

    @parameterized.expand([
        ('produto', 270),
        ('variacao', 270),
        ('imagem', 5000),
    ])
    def test_item_pedido_model_fields_max_length(self, field, max_length):
        item_pedido = self.make_item_pedido()
        setattr(item_pedido, field, 'S' * max_length)

        with self.assertRaises(ValidationError):
            item_pedido.full_clean()
