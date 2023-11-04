from projects.models import Project
from rest_framework import serializers, viewsets
from app.routing import router

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","index","default","name","description","created_by","company"]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

router.register(r'project', ProjectViewSet)