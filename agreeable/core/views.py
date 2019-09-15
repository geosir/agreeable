from django.shortcuts import render

from .models import Document


def index(request):
    return render(request, 'main/index.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'main/signup.html')


def sign(request, docid):
    try:
        document = Document.objects.get(docid=docid)
    except Document.DoesNotExist:
        return render(request, 'main/404.html', status=404)

    name = document.signee
    return render(request, 'main/sign.html', context={'name': name})


def handler404(request, exception, template_name="404.html"):
    return render(request, "404.html", status=404)
