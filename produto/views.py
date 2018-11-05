from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from produto.forms import ProdutoForm, RemoveProdutoForm, PesquisaProdutoForm
from produto.models import Produto

def pesquisa_produto(request):
    form = PesquisaProdutoForm()
    return render(request, 'produto/pesquisa_produto.html', {'form': form})

def exibe_produtos(request):
    form = PesquisaProdutoForm(request.GET)
    if form.is_valid():
        buscaPor = form.cleaned_data['buscaPor']
        lista_de_produtos = Produto.objects\
                                   .filter(nome__icontains=buscaPor)\
                                   .order_by('nome')
        pagina = request.GET.get('pagina', 1)
        paginator = Paginator(lista_de_produtos, 5)
        try:
            produtos = paginator.page(pagina)
        except PageNotAnInteger:
            produtos = paginator.page(1)
        except EmptyPage:
            produtos = paginator.page(paginator.num_pages)

        form = PesquisaProdutoForm()
        return render(request, 'produto/pesquisa_produto.html', {'form': form,
                                                                'produtos': produtos,
                                                                'buscaPor': buscaPor})
    else:
        raise ValueError('Ocorreu um erro inesperado ao validar o form de pesquisa de produto.')


# @login_required
def cadastra_produto(request):

    # Aqui recuperamos o parâmetro de requisição produto_id.
    # Se este parâmetro de requisição existir no objeto request, significa que se trata de uma alteração.
    # Caso contrário, trata-se de uma inclusão.
    produto_id = request.POST.get('produto_id')

    if request.POST:
        # Se o parâmetro veio, trata-se de uma alteração.
        if produto_id:
            acao = 'alteracao'
            # Recupera um objeto Produto ou gera o erro 404
            produto = get_object_or_404(Produto, pk=produto_id)

            # Como se trata de uma alteração, o objeto ProdutoForm é instanciado utilizando
            # os dados provenientes do banco de dados (instance=produto) e, em seguida,
            # essas informações são atualizadas utilizando os dados submetidos pelo usuário (request.POST).
            form_produto = ProdutoForm(request.POST, instance=produto)
        else:
            acao = 'inclusao'
            form_produto = ProdutoForm(request.POST)

        # A linha de código abaixo testa se os dados constantes do form estão corretos.
        # As regras de validação foram definidas no form (ProdutoForm). Os campos categoria, nome, preco e
        # data_cadastro são de preenchimento obrigatório (required=True). E o campo preco deve obedecer a
        # uma expressão regular (veja em ProdutoForm)

        # Observe que o comando if abaixo não possui o "else". Caso ocorra um erro de validação a página
        # cadastra_produto.html será exibida novamente juntamente com as mensagens de erro.
        if form_produto.is_valid():
            # O método save() de ModelForm salva o produto (inclui ou altera) no banco de dados e retorna
            # um objeto do tipo Produto.
            produto = form_produto.save(commit=False)

            # Se a variável produto_id for diferente de None então trata-se de uma alteração
            if produto_id:
                produto.save()
                # Gera uma mensagem que será exibida pela página exibe_produto.html através do framework de mensagens.
                messages.add_message(request, messages.INFO, 'Produto alterado com sucesso.')
            else:
                produto.user = request.user
                produto.save()
                messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso.')

            # Aqui efetuamos um redirect para evitar que um mesmo produto seja cadastrado mais
            # de uma vez caso o usuário aperte a tecla F5 após cadastrar o produto.
            return redirect('produto:exibe_produto', id=produto.id)
    else:
        # Ao chegar uma requisição do tipo GET, a página cadastra_produto.html é exibida.
        acao = 'inclusao'
        form_produto = ProdutoForm()

    # Caso ocorra um erro de validação a página cadastra_produto.html será exibida com as
    # mensagens de erro de validação.
    return render(request, 'produto/cadastra_produto.html', {'form': form_produto,
                                                             'acao': acao})


def exibe_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)

    # Aqui instanciamos o objeto remove_produto_form para que os botões de edição e de remoção sejam exibidos.
    remove_produto_form = RemoveProdutoForm(initial={'produto_id': id})
    return render(request, 'produto/exibe_produto.html', {'produto': produto,
                                                          'remove_produto_form': remove_produto_form})

def edita_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    form_produto = ProdutoForm(instance=produto)
    form_produto.fields['produto_id'].initial = produto.id
    return render(request, 'produto/cadastra_produto.html', {'form': form_produto,
                                                             'acao': 'alteracao'})
def remove_produto(request):
    remove_produto_form = RemoveProdutoForm(request.POST)
    if remove_produto_form.is_valid():
        produto_id = remove_produto_form.cleaned_data['produto_id']
        produto = get_object_or_404(Produto, pk=produto_id)
        if produto.user == request.user:
            produto.delete()
            messages.add_message(request, messages.INFO, 'Produto removido com sucesso.')
        else:
            messages.add_message(request, messages.ERROR, 'Você não está autorizado a remover este produto.')

        return render(request, 'produto/exibe_produto.html', {'produto': produto,
                                                              'remove_produto_form': None})
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar remover um produto')






