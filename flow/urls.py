
from django.urls import path

from flow.views import *

app_name = "flow"
urlpatterns = [
    path("", flow_index, name="flow_index"),
    path("<int:flow_id>/", flow_read, name="flow_read"),
    path("<int:flow_id>/task/<int:task_id>/", flow_read, name="flow_read"),
    path("create_task/", flow_create_task, name="flow_create_task"),
    path("a/carozzi/", flow_carozzi_index, name="carozzi"),
    path("a/carozzi/<int:pitch_id>/", flow_carozzi_index, name="carozzi"),
    path("<int:flow_id>/task/<int:task_id>/send_email/", flow_send_email, name="send_mail")
]