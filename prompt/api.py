from prompt.models import Prompt
from rest_framework import serializers, viewsets
from app.routing import router

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ["id","index","name","prompt"]

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer

router.register(r'prompt', PromptViewSet)