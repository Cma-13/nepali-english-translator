from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .documents import build_translation_docx
from .forms import PreetiForm, TranslateForm
from .models import Translation
from .preeti import preeti_to_unicode
from .services import TranslationError, translate_text

DOCX_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


@login_required
def translate(request):
    translation = None
    error = None

    if request.method == "POST":
        form = TranslateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            text = preeti_to_unicode(data["text"]) if data["is_preeti"] else data["text"]
            try:
                result = translate_text(text, data["direction"], data["tone"])
                translation = Translation.objects.create(
                    user=request.user,
                    source_text=text,
                    translated_text=result,
                    direction=data["direction"],
                    tone=data["tone"],
                )
            except TranslationError as e:
                error = str(e)
    else:
        form = TranslateForm()

    return render(request, "translator/translate.html", {
        "form": form,
        "translation": translation,
        "error": error,
    })


@login_required
def preeti_converter(request):
    result = None

    if request.method == "POST":
        form = PreetiForm(request.POST)
        if form.is_valid():
            result = preeti_to_unicode(form.cleaned_data["text"])
    else:
        form = PreetiForm()

    return render(request, "translator/preeti.html", {"form": form, "result": result})


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


@login_required
def history_download(request, pk):
    translation = get_object_or_404(Translation, pk=pk, user=request.user)
    filename = f"translation-{translation.created_at:%Y-%m-%d}-{translation.pk}.docx"

    response = HttpResponse(build_translation_docx(translation), content_type=DOCX_CONTENT_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
