import django_filters.rest_framework
from .models import Pitch
from rest_framework import serializers, viewsets
from app.routing import router

class PitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = ["pk", "author_name", "author_email", "startup_name", "startup_level"]

class PitchViewSet(viewsets.ModelViewSet):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['author_name', 'author_email', 'startup_name', 'startup_level']

router.register(r'pitch', PitchViewSet)