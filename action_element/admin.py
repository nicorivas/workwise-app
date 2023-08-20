from django.contrib import admin

from .models import ActionElement, ActionElementType, ActionElementAgentCall, ActionElementMessage, ActionElementTextInput

admin.site.register(ActionElement)
admin.site.register(ActionElementType)
admin.site.register(ActionElementAgentCall)
admin.site.register(ActionElementMessage)
admin.site.register(ActionElementTextInput)