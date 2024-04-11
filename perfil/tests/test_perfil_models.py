from django.core.exceptions import ValidationError

from parameterized import parameterized

from produto.tests.test_base import MyBaseTest

from perfil.models import User, Perfil


class PerfilModelsTest(MyBaseTest):
    def test_perfil_string_representation(self):
        perfil = self.make_perfil()
        perfil.user.first_name = 'Jao'
        perfil.user.last_name = 'Ferrer'
        perfil.save()
        self.assertEqual(
            str(perfil),
            f'Usuario {perfil.user.first_name} {perfil.user.last_name}'
        )

    @parameterized.expand([
        ('cpf', 12),
        ('endereco', 55),
        ('numero', 10),
        ('complemento', 35),
        ('bairro', 45),
        ('cep', 10),
        ('cidade', 35),
    ])
    def test_perfil_model_fields_max_length(self, field, max_length):
        perfil = self.make_perfil()
        setattr(perfil, field, 'S' * max_length)

        with self.assertRaises(ValidationError):
            perfil.full_clean()

    def test_perfil_model_receive_a_duplicate_cpf(self):
        self.make_perfil()
        user = User.objects.create(username='cpf-test', password='123455')
        perfil_2 = Perfil.objects.create(
            user=user,
            idade=34,
            data_nascimento='1993-03-21',
            cpf='98739945057',
            endereco='Av. Brasil',
            numero='100',
            complemento='A',
            bairro='Centro',
            cep='37410045',
            cidade='Cajuru',
            estado='MG'
        )

        with self.assertRaisesMessage(ValidationError, 'CPF já existe.'):
            perfil_2.full_clean()

    def test_perfil_model_receive_a_invalid_cpf(self):
        perfil = self.make_perfil()
        perfil.cpf = '11133322245'

        with self.assertRaisesMessage(ValidationError, 'Digite um CPF válido'):
            perfil.full_clean()
