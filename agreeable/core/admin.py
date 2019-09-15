from django.contrib import admin

# Register your models here.
from .models import Document, Signer

admin.site.register(Document)
admin.site.register(Signer)
