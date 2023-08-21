from django.contrib import admin

from .models import InstructionType, Instruction, Message, MessageBlock

admin.site.register(Instruction)
admin.site.register(InstructionType)
admin.site.register(Message)
admin.site.register(MessageBlock)