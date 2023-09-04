from django.urls import path

from .views import ActionElementCreateView, ActionElementReadView, ActionElementUpdateView, ActionElementDeleteView, ActionElementCallView

app_name = "action_element"

urlpatterns = [
    path("<int:instruction_type_id>/action_element/create", ActionElementCreateView.as_view(), name="create"),
    path("<int:instruction_type_id>/action_element/<int:action_element_id>/read", ActionElementReadView.as_view(), name="read"),
    path("<int:instruction_type_id>/action_element/<int:action_element_id>/update", ActionElementUpdateView.as_view(), name="update"),
    path("<int:instruction_type_id>/action_element/delete", ActionElementDeleteView.as_view(), name="delete"),
    path("<int:instruction_id>/action_element/<int:action_element_id>/call", ActionElementCallView.as_view(), name="call"),
]