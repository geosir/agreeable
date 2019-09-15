from django.shortcuts import render
from django.http import JsonResponse

import uuid
import json
import urllib.request
from watson_developer_cloud import VisualRecognitionV3

from .models import Document, Signer


def index(request):
    return render(request, 'main/index.html')


def signup(request):
    if request.method == 'POST':
        signer, _ = Signer.objects.get_or_create(
            email=request.POST.get('email'),
            first_name=request.POST.get('first-name'),
            last_name=request.POST.get('last-name'),
        )

        return render(request, 'main/addkey.html', context={'email': request.POST.get('email')})

    return render(request, 'main/signup.html')


def validatePreview(request):
    if request.method == 'POST':
        img_data = request.POST.get('image')
        name = str(uuid.uuid4())

        response = urllib.request.urlopen(img_data)
        with open("images/" + name + ".png", "wb") as fh:
            fh.write(response.file.read())

        visual_recognition = VisualRecognitionV3(
            '2018-03-19',
            iam_apikey='GfBGcjYPrd-38OXXTbV1uPjKZ5Xp4o-20av0onxqqUIF')

        classes_result = visual_recognition.classify(images_file=open("images/" + name + ".png", 'rb')).get_result()

        classes = [(c['class'], c['score']) for c in classes_result["images"][0]["classifiers"][0]["classes"]]
        classes = sorted(classes, key=lambda x: x[1], reverse=True)

        top = [c[0] for c in classes[:5]]

        return JsonResponse({'status': 'ok', 'top': top})


def addkey(request):
    if request.method == 'POST':
        img_data = request.POST.get('image')
        name = str(uuid.uuid4())

        response = urllib.request.urlopen(img_data)
        with open("images/" + name + ".png", "wb") as fh:
            fh.write(response.file.read())

        visual_recognition = VisualRecognitionV3(
            '2018-03-19',
            iam_apikey='GfBGcjYPrd-38OXXTbV1uPjKZ5Xp4o-20av0onxqqUIF')

        classes_result = visual_recognition.classify(images_file=open("images/" + name + ".png", 'rb')).get_result()

        classes = [(c['class'], c['score']) for c in classes_result["images"][0]["classifiers"][0]["classes"]]
        classes = sorted(classes, key=lambda x: x[1], reverse=True)

        top = [c for c in classes[:5]]

        signer = Signer.objects.get(email=request.POST.get('email'))
        signer.visual_fingerprint = json.dumps(top)
        signer.save()

        return JsonResponse({'status': 'ok'})


def done(request):
    return render(request, 'main/done.html')


def sign(request, docid):
    try:
        document = Document.objects.get(docid=docid)
    except Document.DoesNotExist:
        return render(request, 'main/404.html', status=404)

    name = document.signee
    return render(request, 'main/sign.html', context={'name': name})


def handler404(request, exception, template_name="404.html"):
    return render(request, "404.html", status=404)
