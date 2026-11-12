from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import TranslateForm
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
            except TranslationError as e:
                error = str(e)
    else:
        form = TranslateForm()

    return render(request, "translator/translate.html", {
        "form": form,
        "result": result,
        "error": error,
    })