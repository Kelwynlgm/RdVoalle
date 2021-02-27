from django.db import models


class Clientes(models.Model):
    id = models.AutoField("ID", auto_created=True, primary_key=True, serialize=False)
    nome = models.CharField("Nome", max_length=100)
    telefone = models.CharField("Telefone", max_length=30)
    email = models.EmailField("Email", unique=True)
    cidade = models.CharField("Cidade", max_length=30)

    class Meta:
        verbose_name = 'Cliente'

    def __str__(self):
        return self.nome
