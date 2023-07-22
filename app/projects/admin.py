from django.contrib import admin

# Register your models here.
from .models import Project, Message

admin.site.register(Project)
admin.site.register(Message)
