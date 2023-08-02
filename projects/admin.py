from django.contrib import admin

from .models import Project, Message, Instruction#, Comment

admin.site.register(Project)
admin.site.register(Message)
admin.site.register(Instruction)
#admin.site.register(Comment)