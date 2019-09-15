from django.db import models

# Create your models here.
class Document(models.Model):
    docid = models.CharField(max_length=128, primary_key=True)
    signee = models.CharField(max_length=64, null=False)

