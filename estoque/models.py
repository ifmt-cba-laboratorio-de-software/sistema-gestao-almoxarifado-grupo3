# estoque/models.py

from django.db import models
from django.contrib.auth.models import User

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100) # Nome/Razão Social
    cnpj = models.CharField("CNPJ", max_length=18, blank=True, null=True)
    contato = models.CharField("Pessoa de Contato", max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome

