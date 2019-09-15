from django.db import models


# Create your models here.
class Document(models.Model):
    docid = models.CharField(max_length=128, primary_key=True)
    signer = models.ForeignKey('Signer', on_delete=models.SET_NULL, null=True)
    terms = models.TextField()
    signed = models.BooleanField(default=False)


class Signer(models.Model):
    email = models.CharField(max_length=64, primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    visual_fingerprint = models.TextField(blank=True)
