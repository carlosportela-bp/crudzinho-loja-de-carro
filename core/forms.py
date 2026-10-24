from django import forms

from .models import Estoque, Vendedor


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nome', 'numero_vendas']


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['tipo_veiculo', 'consignado']
