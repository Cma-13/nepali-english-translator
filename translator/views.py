from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TranslateForm
from .models import Translation
from .services import TranslationError, translate_text


@login_required
def translate(request):
    result = None
    error = None

    if request.method == "POST":
        form = TranslateForm(request.POST)
        if form.is_valid():
            try:
                result = translate_text(**form.cleaned_data)
                Translation.objects.create(
                    user=request.user,
                    source_text=form.cleaned_data["text"],
                    translated_text=result,
                    direction=form.cleaned_data["direction"],
                    tone=form.cleaned_data["tone"],
                )
            except TranslationError as e:
                error = str(e)
    else:
        form = TranslateForm()

    return render(request, "translator/translate.html", {
        "form": form,
        "result": result,
        "error": error,
    })


@login_required
def history(request):
    translations = Translation.objects.filter(user=request.user)
    page = Paginator(translations, 10).get_page(request.GET.get("page"))
    return render(request, "translator/history.html", {"page": page})


@login_required
def history_detail(request, pk):
    translation = get_object_or_404(Translation, pk=pk, user=request.user)
    return render(request, "translator/history_detail.html", {"translation": translation})


@login_required
@require_POST
def history_delete(request, pk):
    translation = get_object_or_404(Translation, pk=pk, user=request.user)
    translation.delete()
    return redirect("history")
