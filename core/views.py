from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CarroVendaForm, EstoqueForm, VendedorForm
from .models import CarroVenda, Estoque, Vendedor


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
    erro = None
    if request.method == 'POST':
        try:
            vendedor.delete()  # DELETE FROM vendedores WHERE id = ...
            return redirect('vendedor_lista')
        except ProtectedError:
            erro = 'Não é possível excluir: este vendedor tem vendas registradas.'
    return render(request, 'core/vendedor_excluir.html', {'vendedor': vendedor, 'erro': erro})


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
    erro = None
    if request.method == 'POST':
        try:
            veiculo.delete()  # DELETE FROM estoque WHERE id_carro = ...
            return redirect('estoque_lista')
        except ProtectedError:
            erro = 'Não é possível excluir: este veículo tem vendas registradas.'
    return render(request, 'core/estoque_excluir.html', {'veiculo': veiculo, 'erro': erro})


# Consultar vendas (JOIN com vendedores e estoque, filtro por vendedor e tipo)
@login_required
def venda_lista(request):
    vendedor = request.GET.get('vendedor', '')
    tipo = request.GET.get('tipo', '')
    vendas = CarroVenda.objects.select_related('vendedor', 'carro')  # JOIN vendedores e estoque
    if vendedor:
        vendas = vendas.filter(vendedor_id=vendedor)  # WHERE idvendedores = ...
    if tipo:
        vendas = vendas.filter(carro__tipo_veiculo=tipo)  # WHERE estoque.tipo_veiculo = ...
    contexto = {
        'vendas': vendas,
        'vendedores': Vendedor.objects.all(),
        'tipos': Estoque.TIPOS,
        'vendedor': vendedor,
        'tipo': tipo,
    }
    return render(request, 'core/venda_lista.html', contexto)


# Cadastrar venda
@login_required
def venda_criar(request):
    form = CarroVendaForm(request.POST or None)
    if form.is_valid():
        form.save()  # INSERT INTO carros_vendas ...
        return redirect('venda_lista')
    return render(request, 'core/venda_form.html', {'form': form, 'titulo': 'Nova venda'})


# Atualizar venda
@login_required
def venda_editar(request, id):
    venda = get_object_or_404(CarroVenda, token_venda=id)
    form = CarroVendaForm(request.POST or None, instance=venda)
    if form.is_valid():
        form.save()  # UPDATE carros_vendas SET ... WHERE token_venda = ...
        return redirect('venda_lista')
    return render(request, 'core/venda_form.html', {'form': form, 'titulo': 'Editar venda'})


# Excluir venda
@login_required
def venda_excluir(request, id):
    venda = get_object_or_404(CarroVenda, token_venda=id)
    if request.method == 'POST':
        venda.delete()  # DELETE FROM carros_vendas WHERE token_venda = ...
        return redirect('venda_lista')
    return render(request, 'core/venda_excluir.html', {'venda': venda})
