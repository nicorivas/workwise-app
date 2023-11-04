from django.contrib import admin

from .models import Document, DocumentElement, DocumentSource

admin.site.register(Document)
admin.site.register(DocumentElement)
admin.site.register(DocumentSource)