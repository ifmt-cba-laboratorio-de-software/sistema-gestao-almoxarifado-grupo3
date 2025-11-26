from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BasicUserCreationForm(UserCreationForm):
    """Formulário base para criação de usuários finais."""

    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nome",
        widget=forms.TextInput(attrs={"placeholder": "Nome"}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Sobrenome",
        widget=forms.TextInput(attrs={"placeholder": "Sobrenome"}),
    )
    email = forms.EmailField(
        required=True,
        label="E-mail corporativo",
        widget=forms.EmailInput(attrs={"placeholder": "nome@empresa.com"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "username")
        labels = {
            "username": "Usuário",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "nome.sobrenome",
            "password1": "Mínimo de 8 caracteres",
            "password2": "Repita a senha",
        }
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            if name in placeholders:
                field.widget.attrs.setdefault("placeholder", placeholders[name])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
