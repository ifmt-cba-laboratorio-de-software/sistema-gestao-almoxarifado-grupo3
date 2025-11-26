from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BasicUserCreationForm


@login_required
def signup(request):
    """Tela de cadastro para novos usuários internos, acessível apenas no sistema."""
    if not request.user.is_staff:
        messages.error(request, "Você não possui permissão para cadastrar novos usuários.")
        return redirect("index")

    if request.method == "POST":
        form = BasicUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Usuário criado com sucesso! Compartilhe o login com o novo integrante.",
            )
            return redirect("signup")
    else:
        form = BasicUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
