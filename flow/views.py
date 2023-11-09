import openai
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Pitch
from .forms import PitchCreateForm

class FlowCarozziIndexView(View):
    
    def get(self, request, pitch_id=None):

        form = None
        pitch = None

        if pitch_id:
            pitch = Pitch.objects.get(pk=pitch_id)
            form = PitchCreateForm(instance=pitch)
            context = {"form": form, "pitch": pitch}
        else:
            form = PitchCreateForm()

        context = {"form": form, "pitch": pitch}

        return render(request, "flow/index.html", context)

flow_carozzi_index = FlowCarozziIndexView.as_view()

class FlowTranscribe(View):
    
    def post(self, request):

        audio_file = request.FILES['audio']
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        pitch = Pitch.objects.get(pk=request.POST.get("pitch_id"))
        pitch.pitch = transcript["text"]
        pitch.save()

        response = {
            "text":transcript["text"]
        }

        return JsonResponse(response, safe=False)
    
flow_transcribe = FlowTranscribe.as_view()

class FlowAnalyse(View):

    def post(self, request):

        pitch = Pitch.objects.get(pk=request.POST.get("pitch_id"))
        pitch.analyse(request)
        pitch.save()

        response = {
            "text": pitch.pitch_analysis_short
        }

        return JsonResponse(response, safe=False)

flow_analyse = FlowAnalyse.as_view()