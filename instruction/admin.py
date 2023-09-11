from django.contrib import admin

from .models import *

admin.site.register(Instruction)
admin.site.register(InstructionType)
admin.site.register(InstructionElement)
admin.site.register(InstructionElementMessage)
admin.site.register(InstructionElementType)
admin.site.register(Message)
admin.site.register(MessageBlock)