from django.test import TestCase
from django.urls import reverse


class PagamentoURLsTest(TestCase):

    def test_pagamento_inicio_url_is_correct(self):
        url = reverse('pagamento:inicio', kwargs={'pk': 1})
        self.assertEqual(url, '/pagar/inicio/1')

    def test_pagamento_controle_pagamento_credito_is_correct(self):
        url = reverse('pagamento:credito', kwargs={'pk': 1})
        self.assertEqual(url, '/pagar/controle-pagamento/1/credito')

    def test_pagamento_controle_pagamento_boleto_is_correct(self):
        url = reverse('pagamento:boleto', kwargs={'pk': 1})
        self.assertEqual(url, '/pagar/controle-pagamento/1/boleto')

    def test_pagamento_controle_pagamento_pix_is_correct(self):
        url = reverse('pagamento:pix', kwargs={'pk': 1})
        self.assertEqual(url, '/pagar/controle-pagamento/1/pix')
