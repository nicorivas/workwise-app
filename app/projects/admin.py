from django.contrib import admin

# Register your models here.
from .models import Project, Message, Instruction, Document

admin.site.register(Project)
admin.site.register(Message)
admin.site.register(Document)
admin.site.register(Instruction)