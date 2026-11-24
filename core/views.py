from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from . import dashboard as sql
from .forms import CarroVendaForm, EstoqueForm, VendedorForm
from .models import CarroVenda, Estoque, Vendedor


@login_required
def home(request):
    return render(request, 'core/home.html')


def brl(valor):
    """Formata um número como moeda: 1314000 -> 'R$ 1.314.000,00'."""
    if valor is None:
        return '—'
    texto = f'{float(valor):,.2f}'  # 1,314,000.00
    return 'R$ ' + texto.replace(',', '_').replace('.', ',').replace('_', '.')


# Dashboard: todos os números e gráficos vêm de consultas SQL reais (core/dashboard.py)
@login_required
def dashboard(request):
    resumo = sql.consultar_um(sql.SQL_RESUMO_VENDAS)
    maior = sql.consultar_um(sql.SQL_MAIOR_VENDA)
    menor = sql.consultar_um(sql.SQL_MENOR_VENDA)
    disponivel = sql.consultar_um(sql.SQL_ESTOQUE_DISPONIVEL)
    destaque = sql.consultar_um(sql.SQL_VENDEDOR_DESTAQUE)

    por_mes = sql.consultar(sql.SQL_VENDAS_POR_MES)
    por_vendedor = sql.consultar(sql.SQL_FATURAMENTO_POR_VENDEDOR)
    por_tipo = sql.consultar(sql.SQL_VENDAS_POR_TIPO)
    marcas = sql.consultar(sql.SQL_MARCAS_MAIS_VENDIDAS)

    media_vendedor = sql.consultar_um(sql.SQL_MEDIA_POR_VENDEDOR)['media']
    acima_media = sql.consultar(sql.SQL_VENDEDORES_ACIMA_DA_MEDIA)
    estoque_tipo = sql.consultar(sql.SQL_ESTOQUE_POR_TIPO)

    kpis = [
        {
            'titulo': 'Faturamento total',
            'valor': brl(resumo['faturamento']),
            'detalhe': f"{resumo['total_vendas']} veículos vendidos",
            'tags': ['SUM', 'COUNT'],
            'sql': sql.SQL_RESUMO_VENDAS,
        },
        {
            'titulo': 'Ticket médio',
            'valor': brl(resumo['ticket_medio']),
            'detalhe': 'valor médio por venda',
            'tags': ['AVG'],
            'sql': sql.SQL_RESUMO_VENDAS,
        },
        {
            'titulo': 'Maior venda',
            'valor': brl(maior['valor_venda']) if maior else '—',
            'detalhe': f"{maior['veiculo']} · {maior['vendedor']}" if maior else 'sem vendas',
            'tags': ['MAX', 'SUBQUERY', 'JOIN'],
            'sql': sql.SQL_MAIOR_VENDA,
        },
        {
            'titulo': 'Menor venda',
            'valor': brl(menor['valor_venda']) if menor else '—',
            'detalhe': f"{menor['veiculo']} · {menor['vendedor']}" if menor else 'sem vendas',
            'tags': ['MIN', 'SUBQUERY', 'JOIN'],
            'sql': sql.SQL_MENOR_VENDA,
        },
        {
            'titulo': 'Veículos disponíveis',
            'valor': disponivel['quantidade'],
            'detalhe': (
                f"{brl(disponivel['valor_total'])} em estoque · "
                f"de {brl(disponivel['mais_barato'])} a {brl(disponivel['mais_caro'])}"
            ),
            'tags': ['MIN', 'MAX', 'SUBQUERY'],
            'sql': sql.SQL_ESTOQUE_DISPONIVEL,
        },
        {
            'titulo': 'Vendedor destaque',
            'valor': destaque['nome'] if destaque else '—',
            'detalhe': (
                f"{destaque['vendas']} vendas · {brl(destaque['faturamento'])}" if destaque else 'sem vendas'
            ),
            'tags': ['JOIN', 'GROUP BY'],
            'sql': sql.SQL_VENDEDOR_DESTAQUE,
        },
    ]

    # dados dos gráficos (vão para o JavaScript via json_script)
    graficos = {
        'mes': {
            'labels': [l['mes'] for l in por_mes],
            'faturamento': [float(l['faturamento']) for l in por_mes],
            'vendas': [l['vendas'] for l in por_mes],
        },
        'vendedor': {
            'labels': [l['nome'] for l in por_vendedor],
            'faturamento': [float(l['faturamento']) for l in por_vendedor],
        },
        'tipo': {
            'labels': [l['tipo'] for l in por_tipo],
            'vendas': [l['vendas'] for l in por_tipo],
        },
        'marcas': {
            'labels': [l['marca'] for l in marcas],
            'vendas': [l['vendas'] for l in marcas],
        },
    }

    for linha in acima_media:
        for campo in ('faturamento', 'menor_venda', 'maior_venda'):
            linha[campo] = brl(linha[campo])
    for linha in estoque_tipo:
        for campo in ('menor_preco', 'maior_preco', 'preco_medio'):
            linha[campo] = brl(linha[campo])

    contexto = {
        'kpis': kpis,
        'graficos': graficos,
        'sql_mes': sql.SQL_VENDAS_POR_MES,
        'sql_vendedor': sql.SQL_FATURAMENTO_POR_VENDEDOR,
        'sql_tipo': sql.SQL_VENDAS_POR_TIPO,
        'sql_marcas': sql.SQL_MARCAS_MAIS_VENDIDAS,
        'media_vendedor': brl(media_vendedor),
        'acima_media': acima_media,
        'sql_acima_media': sql.SQL_VENDEDORES_ACIMA_DA_MEDIA,
        'estoque_tipo': estoque_tipo,
        'sql_estoque_tipo': sql.SQL_ESTOQUE_POR_TIPO,
    }
    return render(request, 'core/dashboard.html', contexto)


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
