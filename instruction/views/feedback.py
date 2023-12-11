import logging

from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from instruction.models.feedback import Feedback

class FeedbackReadView(View):

    def get(self, request, instruction_id:int, instruction_element_id:int):
        logging.warn(f"FeedbackReadView.get: {request.POST}")
        try:
            feedback = Feedback.objects.get(instruction=instruction_id, instruction_element=instruction_element_id)
        except Feedback.DoesNotExist:
            logging.warn(f"Feedback does not exist for instruction_id: {instruction_id} and instruction_element_id: {instruction_element_id}")
            feedback = Feedback.objects.create(instruction_id=instruction_id, instruction_element_id=instruction_element_id)
        context = {"feedback": feedback}
        return render(request, "components/instructionElementFeedback/instructionElementFeedback.html", context)
    
    def post(self, request, instruction_id:int, instruction_element_id:int):
        logging.warn(f"FeedbackReadView.post: {request.POST}")
        feedback = Feedback.objects.get(instruction=instruction_id, instruction_element=instruction_element_id)
        feedback.text = request.POST.get("text", "")
        feedback.save()
        context = {"feedback": feedback}
        return render(request, "components/instructionElementFeedback/instructionElementFeedback.html", context)

feedback_read_view = FeedbackReadView.as_view()