from django.urls import path

from .views import ElementCreateView, ElementReadView, ElementUpdateView, ElementDeleteView, ElementCallView

app_name = "action_element"

urlpatterns = [
    path("<int:instruction_id>/element/create", ElementCreateView.as_view(), name="create"),
    path("<int:instruction_id>/element/<int:action_element_id>/read", ElementReadView.as_view(), name="read"),
    path("<int:instruction_id>/element/<int:action_element_id>/update", ElementUpdateView.as_view(), name="update"),
    path("<int:instruction_id>/element/delete", ElementDeleteView.as_view(), name="delete"),
    path("<int:instruction_id>/element/<int:action_element_id>/call", ElementCallView.as_view(), name="call"),
]