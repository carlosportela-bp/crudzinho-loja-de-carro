from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EstoqueForm, VendedorForm
from .models import Estoque, Vendedor


@login_required
def home(request):
    return render(request, 'core/home.html')


# Consultar (com filtro por nome)
@login_required
def vendedor_lista(request):
    busca = request.GET.get('busca', '')
    vendedores = Vendedor.objects.all()
    if busca:
        vendedores = vendedores.filter(nome__icontains=busca)  # WHERE nome ILIKE '%busca%'
    return render(request, 'core/vendedor_lista.html', {'vendedores': vendedores, 'busca': busca})


# Cadastrar
@login_required
def vendedor_criar(request):
    form = VendedorForm(request.POST or None)
    if form.is_valid():
        form.save()  # INSERT INTO vendedores ...
        return redirect('vendedor_lista')
    return render(request, 'core/vendedor_form.html', {'form': form, 'titulo': 'Novo vendedor'})


# Atualizar
@login_required
def vendedor_editar(request, id):
    vendedor = get_object_or_404(Vendedor, id=id)
    form = VendedorForm(request.POST or None, instance=vendedor)
    if form.is_valid():
        form.save()  # UPDATE vendedores SET ... WHERE id = ...
        return redirect('vendedor_lista')
    return render(request, 'core/vendedor_form.html', {'form': form, 'titulo': 'Editar vendedor'})


# Excluir
@login_required
def vendedor_excluir(request, id):
    vendedor = get_object_or_404(Vendedor, id=id)
    if request.method == 'POST':
        vendedor.delete()  # DELETE FROM vendedores WHERE id = ...
        return redirect('vendedor_lista')
    return render(request, 'core/vendedor_excluir.html', {'vendedor': vendedor})


# Consultar estoque (com filtro por tipo e consignado)
@login_required
def estoque_lista(request):
    tipo = request.GET.get('tipo', '')
    consignado = request.GET.get('consignado', '')
    veiculos = Estoque.objects.all()
    if tipo:
        veiculos = veiculos.filter(tipo_veiculo=tipo)  # WHERE tipo_veiculo = ...
    if consignado:
        veiculos = veiculos.filter(consignado=(consignado == 'sim'))  # WHERE consignado = TRUE/FALSE
    contexto = {
        'veiculos': veiculos,
        'tipos': Estoque.TIPOS,
        'tipo': tipo,
        'consignado': consignado,
    }
    return render(request, 'core/estoque_lista.html', contexto)


# Cadastrar no estoque
@login_required
def estoque_criar(request):
    form = EstoqueForm(request.POST or None)
    if form.is_valid():
        form.save()  # INSERT INTO estoque ...
        return redirect('estoque_lista')
    return render(request, 'core/estoque_form.html', {'form': form, 'titulo': 'Novo veículo'})


# Atualizar estoque
@login_required
def estoque_editar(request, id):
    veiculo = get_object_or_404(Estoque, id_carro=id)
    form = EstoqueForm(request.POST or None, instance=veiculo)
    if form.is_valid():
        form.save()  # UPDATE estoque SET ... WHERE id_carro = ...
        return redirect('estoque_lista')
    return render(request, 'core/estoque_form.html', {'form': form, 'titulo': 'Editar veículo'})


# Excluir do estoque
@login_required
def estoque_excluir(request, id):
    veiculo = get_object_or_404(Estoque, id_carro=id)
    if request.method == 'POST':
        veiculo.delete()  # DELETE FROM estoque WHERE id_carro = ...
        return redirect('estoque_lista')
    return render(request, 'core/estoque_excluir.html', {'veiculo': veiculo})
