from django.urls import path

from .views import CompanyView, CompanySetView, CompanyStrategyView, CompanyValuesView

app_name = "company"

urlpatterns = [
    path("<int:company_id>/", CompanyView.as_view(), name="index"),
    path("<int:company_id>/set", CompanySetView.as_view(), name="set"),
    path("<int:company_id>/strategy", CompanyStrategyView.as_view(), name="strategy"),
    path("<int:company_id>/values", CompanyValuesView.as_view(), name="values"),
]