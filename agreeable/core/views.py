from django.shortcuts import render
from django.http import JsonResponse

import uuid
import json
import math
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

        top = [c for c in classes[:10]]

        signer = Signer.objects.get(email=request.POST.get('email'))
        signer.visual_fingerprint = json.dumps(top)
        signer.save()

        return JsonResponse({'status': 'ok'})


def validate(request):
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

    top = [c for c in classes[:10]]

    signer = Signer.objects.get(email=request.POST.get('email'))
    visual_fingerprint = dict(json.loads(signer.visual_fingerprint))

    # validate
    same_diff = []
    for c, s in top:
        if c in visual_fingerprint:
            same_diff.append(s - visual_fingerprint[c])

    print(same_diff)

    if len(same_diff) < 3:
        return JsonResponse({'status': 'fail'}, status=403)
    if math.sqrt(sum(map(lambda x: x ** 2, same_diff))) > 0.5:
        return JsonResponse({'status': 'fail'}, status=403)

    return JsonResponse({'status': 'ok'})


def asksign(request, docid):
    try:
        document = Document.objects.get(docid=docid, signed=False)
    except Document.DoesNotExist:
        return render(request, 'main/404.html', status=404)

    return render(request, 'main/asksign.html', context={'document': document})


def done(request):
    return render(request, 'main/done.html')


def fail(request):
    return render(request, 'main/fail.html')


def sign_yes(request, docid):
    try:
        document = Document.objects.get(docid=docid, signed=False)
    except Document.DoesNotExist:
        return render(request, 'main/404.html', status=404)

    document.signed = True
    document.save()

    return render(request, 'main/sign_done.html')


def sign_no(request):
    return render(request, 'main/sign_cancel.html')


def sign(request, docid):
    try:
        document = Document.objects.get(docid=docid, signed=False)
    except Document.DoesNotExist:
        return render(request, 'main/404.html', status=404)

    signer = document.signer
    terms = json.loads(document.terms)
    return render(request, 'main/sign.html',
                  context={'name': signer.first_name, 'email': signer.email, 'docid': docid, 'terms': terms})


def handler404(request, exception, template_name="404.html"):
    return render(request, "404.html", status=404)
