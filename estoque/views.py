from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Fornecedor, Item, Movimentacao
from .forms import FornecedorForm, ItemForm, MovimentacaoForm
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def index(request):
    items = Item.objects.all().order_by('descricao')
    paginator = Paginator(items, 20)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'estoque/item_list.html', {'items': items})

@login_required
@permission_required('estoque.add_item', raise_exception=True)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item criado com sucesso.')
            return redirect('index')
    else:
        form = ItemForm()
    return render(request, 'estoque/item_form.html', {'form': form})

@login_required
@permission_required('estoque.change_item', raise_exception=True)
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado com sucesso.')
            return redirect('index')
    else:
        form = ItemForm(instance=item)
    return render(request, 'estoque/item_form.html', {'form': form, 'item': item})

@login_required
@permission_required('estoque.delete_item', raise_exception=True)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    messages.success(request, 'Item removido.')
    return redirect('index')

@login_required
@permission_required('estoque.add_movimentacao', raise_exception=True)
def movimentacao_create(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            mov.usuario = request.user
            mov.save()
            messages.success(request, 'Movimentação registrada.')
            return redirect('index')
    else:
        form = MovimentacaoForm()
    return render(request, 'estoque/movimentacao_form.html', {'form': form})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    movimentos = Movimentacao.objects.filter(item=item).order_by('-data')[:50]
    return render(request, 'estoque/item_detail.html', {'item': item, 'movimentos': movimentos})



# CRUD FORNECEDORES

@login_required
@permission_required('estoque.view_fornecedor', raise_exception=True)
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all().order_by('nome')
    paginator = Paginator(fornecedores, 20)
    page = request.GET.get('page')
    fornecedores = paginator.get_page(page)
    return render(request, 'estoque/fornecedor_list.html', {'fornecedores': fornecedores})

@login_required
@permission_required('estoque.add_fornecedor', raise_exception=True)
def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor criado com sucesso.')
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm()
    return render(request, 'estoque/fornecedor_form.html', {'form': form})

@login_required
@permission_required('estoque.change_fornecedor', raise_exception=True)
def fornecedor_edit(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso.')
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'estoque/fornecedor_form.html', {'form': form, 'fornecedor': fornecedor})

@login_required
@permission_required('estoque.delete_fornecedor', raise_exception=True)
def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    # Verifica se o fornecedor está sendo usado por algum item
    if Item.objects.filter(fornecedor=fornecedor).exists():
        messages.error(request, 'Este fornecedor não pode ser excluído, pois está associado a um ou mais itens.')
        return redirect('fornecedor_list')
        
    fornecedor.delete()
    messages.success(request, 'Fornecedor removido com sucesso.')
    return redirect('fornecedor_list')



# ================================
# VIEWS DE BUSCA ITEM E FORNECEDOR(HTMX)
# ================================

@login_required
def buscar_item(request):
    search_text = request.GET.get('q', '').strip()

    if search_text:
        # Usamos Q para buscar no código OU na descrição (icontains não diferencia maiúsculas/minúsculas)
        items = Item.objects.filter(
            Q(codigo__icontains=search_text) | 
            Q(descricao__icontains=search_text)
        ).order_by('descricao')
    else:
        # Se a busca estiver vazia, retorna tudo (limitado para não sobrecarregar)
        items = Item.objects.all().order_by('descricao')[:50] 

    # Renderiza APENAS o template parcial com os resultados
    return render(request, 'estoque/partials/tabela_itens.html', {'items': items})


@login_required
@permission_required('estoque.view_fornecedor', raise_exception=True)
def buscar_fornecedor(request):
    search_text = request.GET.get('q', '').strip()

    if search_text:
        # Busca por Nome, CNPJ ou Email
        fornecedores = Fornecedor.objects.filter(
            Q(nome__icontains=search_text) |
            Q(cnpj__icontains=search_text) |
            Q(email__icontains=search_text)
        ).order_by('nome')
    else:
        fornecedores = Fornecedor.objects.all().order_by('nome')[:50]

    # Renderiza APENAS o template parcial
    return render(request, 'estoque/partials/tabela_fornecedores.html', {'fornecedores': fornecedores})