from django.contrib import admin

from .models import Document, DocumentElement

admin.site.register(Document)
admin.site.register(DocumentElement)