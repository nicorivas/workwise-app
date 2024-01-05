from django.core.exceptions import ValidationError
import re

class ValidatePasswordStrength:
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not re.findall('[A-Z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.findall('[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")
            
    def get_help_text(self):
        return "La contraseña debe contener al menos una letra minúscula, una letra mayúscula y un carácter especial."
