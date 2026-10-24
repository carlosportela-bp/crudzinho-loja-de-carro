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


class Estoque(models.Model):
    TIPOS = [
        (1, 'Carro'),
        (2, 'Moto'),
        (3, 'Caminhonete'),
    ]

    id_carro = models.AutoField(primary_key=True)
    tipo_veiculo = models.IntegerField(choices=TIPOS)
    consignado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'estoque'
        ordering = ['id_carro']

    def __str__(self):
        return f'#{self.id_carro} - {self.get_tipo_veiculo_display()}'


class CarroVenda(models.Model):
    token_venda = models.AutoField(primary_key=True)
    # chaves estrangeiras: PROTECT impede apagar vendedor/veículo que já tem venda
    vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT, db_column='idvendedores')
    carro = models.ForeignKey(Estoque, on_delete=models.PROTECT, db_column='id_carro')

    class Meta:
        managed = False
        db_table = 'carros_vendas'
        ordering = ['-token_venda']

    def __str__(self):
        return f'Venda {self.token_venda}'
