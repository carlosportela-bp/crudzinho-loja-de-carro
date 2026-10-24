from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vendedores/', views.vendedor_lista, name='vendedor_lista'),
    path('vendedores/novo/', views.vendedor_criar, name='vendedor_criar'),
    path('vendedores/<int:id>/editar/', views.vendedor_editar, name='vendedor_editar'),
    path('vendedores/<int:id>/excluir/', views.vendedor_excluir, name='vendedor_excluir'),
    path('estoque/', views.estoque_lista, name='estoque_lista'),
    path('estoque/novo/', views.estoque_criar, name='estoque_criar'),
    path('estoque/<int:id>/editar/', views.estoque_editar, name='estoque_editar'),
    path('estoque/<int:id>/excluir/', views.estoque_excluir, name='estoque_excluir'),
    path('vendas/', views.venda_lista, name='venda_lista'),
    path('vendas/nova/', views.venda_criar, name='venda_criar'),
    path('vendas/<int:id>/editar/', views.venda_editar, name='venda_editar'),
    path('vendas/<int:id>/excluir/', views.venda_excluir, name='venda_excluir'),
]
