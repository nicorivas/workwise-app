from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from app.routing import router

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router.register(r'users', UserViewSet)