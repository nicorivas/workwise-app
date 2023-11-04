import django_filters.rest_framework
from document.models import Document
from rest_framework import serializers, viewsets
from app.routing import router

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "type", "name", "project", "parent_document", "is_format", "date_published"]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['is_format', 'parent_document_id']

router.register(r'document', DocumentViewSet)