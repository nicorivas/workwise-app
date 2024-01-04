from company.models import Company
from rest_framework import serializers, viewsets
from app.routing import router

class CompanySerializerNormal(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'subdomain']

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'subdomain']

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

router.register(r'company', CompanyViewSet)