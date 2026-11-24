from django import forms

from .models import CarroVenda, Estoque, Vendedor


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nome', 'numero_vendas']


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['marca', 'modelo', 'ano', 'tipo_veiculo', 'preco', 'consignado']


class CarroVendaForm(forms.ModelForm):
    class Meta:
        model = CarroVenda
        fields = ['vendedor', 'carro', 'data_venda', 'valor_venda']
        widgets = {
            'data_venda': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
