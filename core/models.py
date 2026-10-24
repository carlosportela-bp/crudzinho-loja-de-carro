from django.db import models


class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    numero_vendas = models.IntegerField(default=0)

    class Meta:
        managed = False  # a tabela foi criada pelo sql/schema.sql, o Django só usa
        db_table = 'vendedores'
        ordering = ['nome']

    def __str__(self):
        return self.nome
