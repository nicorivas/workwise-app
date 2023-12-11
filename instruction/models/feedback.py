import markdown

from django.db import models
from instruction.models.instruction import Instruction
from instruction.models.instruction_element import InstructionElement
from projects.models import Project
from actions.models import Action
from task.models import Task

class Feedback(models.Model):
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE)
    instruction_element = models.ForeignKey(InstructionElement, on_delete=models.CASCADE)
    text = models.TextField(default="", null=True, blank=True)

    @property
    def html(self):
        # Convert markdown text to html
        html = markdown.markdown(self.text)
        return html