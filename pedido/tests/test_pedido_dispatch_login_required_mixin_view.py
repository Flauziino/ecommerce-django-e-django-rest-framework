from django.urls import reverse, resolve

from pedido import views

from produto.tests.test_base import MyBaseTest


class PedidoDispatchLoginRequiredMixinTest(MyBaseTest):
    def test_pedido_dispatch_login_required_mixin_view_is_correct(self):
        view = views.DispatchLoginRequiredMixin()
        self.assertTrue(issubclass(
            view.__class__, views.DispatchLoginRequiredMixin)
        )

    # unico teste unitario que sera cabivel para esta view
    # como ela n recebe diretamente (ela sozinha), uma request, ela nao tem
    # esse atributo, logo os testes nao passam da sua primeira logica no metodo
    # dispatch.
    # essa view sera testada junto de outras views que estao herdando dela.

    # sera feito testes nas outras views que herdam de dispatchloginrequired
    # para testar o mixin

    # TESTANDO A VIEW PAGAR PARA COBRIR A VIEW DISPATCHLOGINREQUIREDMIXIN

    def test_produto_pagar_view_is_correct(self):
        view = resolve(
            reverse(
                'pedido:pagar', kwargs={'pk': 1}
            )
        )
        self.assertIs(view.func.view_class, views.Pagar)

    def test_produto_pagar_view_will_redirects_if_no_authenticated_user_status_code_302(self):  # noqa: E501
        url = reverse('pedido:pagar', kwargs={'pk': 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, response.url)

    def test_produto_pagar_view_receive_authenticated_user_but_dont_have_pedido_status_code_404(self):  # noqa: E501
        self.get_auth_data()
        url = reverse('pedido:pagar', kwargs={'pk': 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_produto_pagar_view_receive_authenticated_user_and_have_pedido(self):  # noqa: E501
        self.get_auth_data()
        pedido = self.make_pedido()
        url = reverse('pedido:pagar', kwargs={'pk': pedido.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_produto_pagar_view_receive_authenticated_user_and_have_pedido_the_query_set_method_is_correct(self):  # noqa: E501
        # como configurado anteriormente get_auth_data retorna o mesmo usuario
        # que o usuario que foi atrelado a tudo que precisava de usuario na cfg
        # resumindo, o pedido feito pelo make_pedido recebe esse mesmo usuario
        # caso deseje, é possivel fazer tudo manualmente passo a passo

        user = self.get_auth_data()
        pedido = self.make_pedido()
        url = reverse('pedido:pagar', kwargs={'pk': pedido.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user, pedido.user)

    def test_produto_pagar_view_uses_correct_template(self):
        self.get_auth_data()
        pedido = self.make_pedido()

        url = reverse('pedido:pagar', kwargs={'pk': pedido.id})

        response = self.client.get(url)

        self.assertTemplateUsed(response, 'pedido/pagar.html')
