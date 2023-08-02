from django.contrib import admin

from .models import ActionDB, ActionFormElement, ActionFormElementType

admin.site.register(ActionDB)
admin.site.register(ActionFormElement)
admin.site.register(ActionFormElementType)