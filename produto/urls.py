from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('cadastrar/', views.cadastra_produto, name='cadastra_produto'),
    path('exibir/<int:id>/', views.exibe_produto, name='exibe_produto'),
    path('editar/<int:id>/', views.edita_produto, name='edita_produto'),
    path('remover/', views.remove_produto, name='remove_produto'),
    path('pesquisar/', views.pesquisa_produto, name='pesquisa_produto'),
    path('listar/', views.exibe_produtos, name='exibe_produtos'),

    # exibe_produto
    # edita_produto
    # remove_produto
]
