from django.db import models  # type:ignore
from django.contrib.auth.models import User  # type:ignore
from django.forms import ValidationError  # type:ignore

import re
from utils.validador_cpf import valida_cpf


class Perfil(models.Model):
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    ESTADO_CHOICES = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
        ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'), ('GO', 'Goiás'),
        ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'),
        ('PR', 'Paraná'), ('PE', 'Pernambuco'),
        ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'), ('SP', 'São Paulo'),
        ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField(blank=True, null=True)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)

    def __str__(self):
        return f'Usuario {self.user.first_name} {self.user.last_name}'

    def clean(self):
        error_msg = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None

        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_msg['cpf'] = 'CPF já existe.'

        if not valida_cpf(self.cpf):
            error_msg['cpf'] = 'Digite um CPF válido'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_msg['cep'] = 'CEP inválido, digite apenas digitos.'

        if error_msg:
            raise ValidationError(
                error_msg
            )
