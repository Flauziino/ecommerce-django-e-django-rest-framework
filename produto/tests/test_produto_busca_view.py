from django.urls import reverse, resolve
from django.test import RequestFactory

from produto import views
from produto import models

from .test_base import MyBaseTest


class ProdutoBuscaViewTest(MyBaseTest):
    def test_produto_busca_views_function_is_correct(self):
        view = resolve(
            reverse(
                'produto:busca'
            )
        )
        self.assertIs(view.func.view_class, views.Busca)

    def test_produto_busca_view_returns_statuscode_200_OK(self):
        url = reverse('produto:busca') + '?termo=gamer'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_produto_busca_view_returns_queryset_if_no_termo(self):
        # criando um produto para verificar se ele sera retornado em caso
        # de nao haver um termo
        models.Produto.objects.create(
            nome='nome_um',
            descricao_curta='test um',
            descricao_longa='longo test um',
            preco_marketing=15,
            slug='nome-um',
        )
        # pegando um requestfactory e minha view para simular a requisicao
        factory = RequestFactory()
        view = views.Busca.as_view()

        # simulando uma requisiçao GET sem o termo
        request = factory.get('/busca/')
        # criando uma session contendo o termo
        request.session = {'termo': None}

        response = view(request)
        # verificando se recebeu status 200
        self.assertEqual(response.status_code, 200)
        # verificando se o produto existe
        self.assertTrue(models.Produto.objects.exists())
        # verificando a quantidade de items retornados na pagina
        # espera-se um pois foi criado apenas um produto
        self.assertEqual(len(response.context_data['produtos']), 1)
        # verificando se a query set é igual a quantidade de produtos
        # no caso vai ser um, basicamente igual assert anterior, mas feito de
        # outra forma
        self.assertQuerySetEqual(
            response.context_data['produtos'], models.Produto.objects.all()
        )

    def test_produto_busca_view_uses_correct_template(self):
        url = reverse('produto:busca') + '?termo=gamer'
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'produto/lista.html')

    def test_produto_busca_view_can_find_item_by_nome(self):
        # separando os titulos
        nome_um = 'esse é o produto um'
        nome_dois = 'esse é o produto dois'

        # criando produto um e dando o nome um pra ele
        produto_um = models.Produto.objects.create(
            nome=nome_um,
            descricao_curta='test um',
            descricao_longa='longo test um',
            preco_marketing=15,
            slug='nome-um',
        )

        # criando produto dois e dando o nome dois pra ele
        produto_dois = models.Produto.objects.create(
            nome=nome_dois,
            descricao_curta='test dois',
            descricao_longa='longo test dois',
            preco_marketing=15,
            slug='nome-dois',
        )

        # uma pesquisa apenas para produto um
        url_p_um = reverse('produto:busca') + '?termo=um'
        response_p_um = self.client.get(url_p_um)

        # uma pesquisa apenas para produto dois
        url_p_dois = reverse('produto:busca') + '?termo=dois'
        response_p_dois = self.client.get(url_p_dois)

        # uma pesquisa para encontrar os dois produtos
        url = reverse('produto:busca') + '?termo=esse'
        response = self.client.get(url)

        # verificando se temos APENAS o produto um na busca UM
        self.assertIn(produto_um, response_p_um.context['produtos'])
        self.assertNotIn(produto_dois, response_p_um.context['produtos'])

        # verificando se temos APENAS o produto dois na busca dois
        self.assertIn(produto_dois, response_p_dois.context['produtos'])
        self.assertNotIn(produto_um, response_p_dois.context['produtos'])

        # verificando se temos os dois items na busca tres
        self.assertIn(produto_um, response.context['produtos'])
        self.assertIn(produto_dois, response.context['produtos'])

    def test_produto_busca_view_can_find_item_by_descricao_curta(self):
        # separando as descricoes curta
        descricao_um = 'esse é o produto um'
        descricao_dois = 'esse é o produto dois'

        # criando produto um e dando o nome um pra ele
        produto_um = models.Produto.objects.create(
            nome='nome_1',
            descricao_curta=descricao_um,
            descricao_longa='longo test 1',
            preco_marketing=15,
            slug='nome-um',
        )

        # criando produto dois e dando o nome dois pra ele
        produto_dois = models.Produto.objects.create(
            nome='nome_2',
            descricao_curta=descricao_dois,
            descricao_longa='longo test 2',
            preco_marketing=15,
            slug='nome-dois',
        )

        # uma pesquisa apenas para produto um
        url_p_um = reverse('produto:busca') + '?termo=um'
        response_p_um = self.client.get(url_p_um)

        # uma pesquisa apenas para produto dois
        url_p_dois = reverse('produto:busca') + '?termo=dois'
        response_p_dois = self.client.get(url_p_dois)

        # uma pesquisa para encontrar os dois produtos
        url = reverse('produto:busca') + '?termo=esse'
        response = self.client.get(url)

        # verificando se temos APENAS o produto um na busca UM
        self.assertIn(produto_um, response_p_um.context['produtos'])
        self.assertNotIn(produto_dois, response_p_um.context['produtos'])

        # verificando se temos APENAS o produto dois na busca dois
        self.assertIn(produto_dois, response_p_dois.context['produtos'])
        self.assertNotIn(produto_um, response_p_dois.context['produtos'])

        # verificando se temos os dois items na busca tres
        self.assertIn(produto_um, response.context['produtos'])
        self.assertIn(produto_dois, response.context['produtos'])

    def test_produto_busca_view_can_find_item_by_descricao_longa(self):
        # separando as descricoes longa
        descricao_um = 'esse é o produto um longa'
        descricao_dois = 'esse é o produto dois longa'

        # criando produto um e dando o nome um pra ele
        produto_um = models.Produto.objects.create(
            nome='nome_1',
            descricao_curta='curta',
            descricao_longa=descricao_um,
            preco_marketing=15,
            slug='nome-um',
        )

        # criando produto dois e dando o nome dois pra ele
        produto_dois = models.Produto.objects.create(
            nome='nome_2',
            descricao_curta='curta',
            descricao_longa=descricao_dois,
            preco_marketing=15,
            slug='nome-dois',
        )

        # uma pesquisa apenas para produto um
        url_p_um = reverse('produto:busca') + '?termo=um'
        response_p_um = self.client.get(url_p_um)

        # uma pesquisa apenas para produto dois
        url_p_dois = reverse('produto:busca') + '?termo=dois'
        response_p_dois = self.client.get(url_p_dois)

        # uma pesquisa para encontrar os dois produtos
        url = reverse('produto:busca') + '?termo=longa'
        response = self.client.get(url)

        # verificando se temos APENAS o produto um na busca UM
        self.assertIn(produto_um, response_p_um.context['produtos'])
        self.assertNotIn(produto_dois, response_p_um.context['produtos'])

        # verificando se temos APENAS o produto dois na busca dois
        self.assertIn(produto_dois, response_p_dois.context['produtos'])
        self.assertNotIn(produto_um, response_p_dois.context['produtos'])

        # verificando se temos os dois items na busca tres
        self.assertIn(produto_um, response.context['produtos'])
        self.assertIn(produto_dois, response.context['produtos'])
