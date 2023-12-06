from django.urls import path

from .views import CompanyCreateView, CompanySetView, CompanyStrategyView, CompanyValuesView

app_name = "company"

urlpatterns = [
    path("", CompanyCreateView.as_view(), name="create"),
    path("<int:company_id>/", CompanyCreateView.as_view(), name="index"),
    path("<int:company_id>/set", CompanySetView.as_view(), name="set"),
    path("<int:company_id>/strategy", CompanyStrategyView.as_view(), name="strategy"),
    path("<int:company_id>/values", CompanyValuesView.as_view(), name="values"),
]