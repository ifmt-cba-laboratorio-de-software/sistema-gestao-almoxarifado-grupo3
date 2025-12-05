from django import forms
from .models import Fornecedor, Item, Movimentacao
import re

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['item', 'tipo', 'quantidade', 'data_devolucao_prevista']


# NOVO FORMULÁRIO DE FORNECEDOR
class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'contato', 'telefone', 'email']

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        
        # Se o campo estiver vazio (pois é opcional no model), retorna vazio
        if not telefone:
            return telefone

        # Remove tudo que NÃO for número (parênteses, traços, espaços)
        apenas_numeros = re.sub(r'\D', '', telefone)

        # Verifica se tem 10 dígitos (Fixo) ou 11 (Celular)
        if len(apenas_numeros) < 10 or len(apenas_numeros) > 11:
            raise ValidationError("O telefone deve conter o DDD + Número (10 ou 11 dígitos).")
        
        # Retorna o valor original (com a máscara) para salvar bonitinho no banco
        return telefone