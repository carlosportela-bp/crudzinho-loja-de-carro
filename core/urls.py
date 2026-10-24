from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vendedores/', views.vendedor_lista, name='vendedor_lista'),
    path('vendedores/novo/', views.vendedor_criar, name='vendedor_criar'),
    path('vendedores/<int:id>/editar/', views.vendedor_editar, name='vendedor_editar'),
    path('vendedores/<int:id>/excluir/', views.vendedor_excluir, name='vendedor_excluir'),
]
