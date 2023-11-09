
from django.urls import path

from flow.views import *

app_name = "flow"
urlpatterns = [
    path("carozzi/", flow_carozzi_index, name="carozzi"),
    path("carozzi/<int:pitch_id>/", flow_carozzi_index, name="carozzi"),
    path("transcribe/", flow_transcribe, name="transcribe"),
    path("analyse/", flow_analyse, name="analyse")
]