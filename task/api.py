import django_filters.rest_framework
from task.models import Task
from rest_framework import serializers, viewsets
from app.routing import router

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "index", "name", "project", "action"]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'project', 'action']

router.register(r'task', TaskViewSet)