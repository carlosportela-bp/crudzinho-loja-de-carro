from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VendedorForm
from .models import Vendedor


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
