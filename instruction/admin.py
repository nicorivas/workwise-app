from django.contrib import admin
from .models import *

models = [Instruction, InstructionType, InstructionElement, InstructionElementType, InstructionElementMessage, InstructionElementAgentCall, InstructionElementTextInput, InstructionElementRevise, InstructionElementRevision, InstructionElementDocumentLink, InstructionElementChoices, Feedback, Message, MessageBlock]

for model in models:
    admin.site.register(model)