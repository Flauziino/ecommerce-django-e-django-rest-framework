from django.urls import reverse, resolve

from produto import views

from .test_base import MyBaseTest


class ProdutoAdicionarCarrinhoViewTest(MyBaseTest):
    def test_adicionar_carrinho_view_function_is_correct(self):
        view = resolve(
            reverse('produto:adicionarcarrinho')
        )
        self.assertIs(view.func.view_class, views.AdicionarCarrinho)

    def test_produto_adicionar_carrinho_view_returns_statuscode_302_if_not_variacao_id(self):  # noqa: E501
        url = reverse('produto:adicionarcarrinho')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        # checando separadamente a response, passando um follow=true para
        # encontrar a msg de erro caso nao tenha a variacao_id
        response = self.client.get(url, follow=True)
        self.assertIn(
            'Produto não existe',
            response.content.decode('utf-8')
        )

    def test_produto_adicionar_carrinho_view_got_variacao_id(self):
        variacao = self.make_variacao()
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'
        self.client.get(url)

        self.assertEqual(variacao.id, 1)

    def test_produto_adicionar_carrinho_view_got_variacao_id_but_dont_find_a_variacao_and_return_404(self):  # noqa: E501
        variacao = self.make_variacao()
        fake_id = variacao.id + 999999999
        url = reverse('produto:adicionarcarrinho') + f'?vid={fake_id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_produto_adicionar_carrinho_view_got_variacao_id_and_bring_product_name_too(self):  # noqa: E501
        variacao = self.make_variacao()
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'
        self.client.get(url)

        # esse nome em questao é o padrao na hr de realizar a criaçao
        # da variacao ou do produto em si.
        self.assertEqual(variacao.produto.nome, 'Camiseta básica TEST')

    def test_produto_adicionar_carrinho_view_got_variacao_id_and_have_the_right_estoque(self):  # noqa: E501
        variacao = self.make_variacao()
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'
        self.client.get(url)

        self.assertEqual(variacao.estoque, 5)

    def test_produto_adicionar_carrinho_view_got_variacao_id_and_have_the_right_slug(self):  # noqa: E501
        variacao = self.make_variacao()
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'
        self.client.get(url)

        # checando se o produto esta atrelado a variacao por padrao
        # e tambem se a slug esta correta de acordo com nome padrao do
        # produto
        self.assertEqual(variacao.produto.slug, 'camiseta-basica-test')

    def test_produto_adicionar_carrinho_view_got_variacao_id_and_have_a_img(self):  # noqa: E501
        variacao = self.make_variacao()
        # criando uma imagem fake
        image_django = 'test_image.jpg'
        # pegando produto pela variacao
        produto = variacao.produto
        # passando a img fake para o produto
        produto.imagem = image_django
        produto.save()

        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'
        self.client.get(url)

        self.assertEqual(produto.imagem, image_django)

    def test_produto_adicionar_carrinho_view_got_variacao_id_but_dont_have_estoque(self):  # noqa: E501
        variacao = self.make_variacao()
        variacao.estoque = 0
        variacao.save()

        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'
        response = self.client.get(url, follow=True)

        self.assertIn(
            'Estoque insuficiente',
            response.content.decode('utf-8')
        )

    def test_produto_adicionar_carrinho_view_got_variacao_id_and_already_have_a_carrinho(self):  # noqa: E501
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'

        # pegando a session
        session = self.client.session
        # criando o carrinho linkado a session
        session['carrinho'] = {'test': '1'}
        # salvando o carrinho
        session.save()

        self.client.get(url)
        self.assertIn('carrinho', session)

    def test_produto_adicionar_carrinho_view_got_variacao_id_and_variacao_id_is_in_carrinho(self):  # noqa: E501
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'

        # adicionando a variacao ao carrinho
        self.client.get(url)
        self.assertIn('carrinho', self.client.session)

        # verificando se a variacao_id esta no carrinho
        self.assertIn(
            str(variacao.id),
            self.client.session['carrinho']
        )

        # verificando se a quantidade é um ate o momento
        self.assertEqual(
            self.client.session['carrinho'][str(variacao.id)]['quantidade'],
            1
        )

        # adicionando a mesma variacao ao carrinho para ver se a quantidade
        # sera de dois
        self.client.get(url)
        self.assertEqual(
            self.client.session['carrinho'][str(variacao.id)]['quantidade'],
            2
        )

    def test_produto_adicionar_carrinho_view_got_variacao_id_and_variacao_id_is_in_carrinho_and_quantidade_carrinho_gt_variacao_estoque(self):  # noqa: E501
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'

        variacao.estoque = 1
        variacao.save()
        # adicionando uma variacao ao carrinho
        self.client.get(url)
        self.assertIn('carrinho', self.client.session)
        # verificando se a variacao_id esta no carrinho
        self.assertIn(str(variacao.id), self.client.session['carrinho'])
        # verificando se a quantidade é um ate o momento
        self.assertEqual(
            self.client.session['carrinho'][str(variacao.id)]['quantidade'],
            1
        )

        # iniciando os testes reais, sera adicionada mais uma variacao
        # pela logica da view devo receber uma msg de alerta
        # e tb a variacao no carrinho tem que ser igual a do estoque
        # nesse caso, UM
        response = self.client.get(url, follow=True)

        # verificando se a quantidade se manteve 1, pois nao tem mais estoque
        self.assertEqual(
            self.client.session['carrinho'][str(variacao.id)]['quantidade'],
            1
        )
        # verificando se a msg esta na resposta
        self.assertContains(
            response,
            'Estoque insuficiente para 2x no produto'
            ' &quot;Camiseta básica TEST&quot;. Adicionamos 1x no seu carrinho.'  # noqa: E501
        )

    def test_produto_adicionar_carrinho_view_is_all_functional(self):
        # cria variacao
        variacao = self.make_variacao()
        # url contendo o id da variacao
        url = reverse('produto:adicionarcarrinho') + f'?vid={variacao.id}'

        # adicionando duas variacoes para verificar se o preço do produto
        # bate com a quantidade no carrinho
        self.client.get(url)
        response = self.client.get(url, follow=True)

        # verificando a msg de sucesso
        self.assertIn(
            f'Produto {variacao.produto.nome} {variacao.nome} adicionado ao seu '  # noqa: E501
            'carrinho 2x.',
            response.content.decode('utf-8')
        )
        # verificando o total do preco normal (espera-se 300)
        self.assertEqual(
            self.client.session['carrinho']
            [str(variacao.id)]['preco_quantitativo'],
            300
        )
        # verificando o total do preco promocional (espera-se 240)
        self.assertEqual(
            self.client.session['carrinho']
            [str(variacao.id)]['preco_quantitativo_promocional'],
            240
        )
