from django.contrib.auth.models import User
from django.db import models

from company.models import Company

class Record(models.Model):
    voice_record = models.FileField(upload_to="records")
    language = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("record_detail", kwargs={"id": str(self.id)})

class Project(models.Model):

    index = models.IntegerField(default=0)
    default = models.BooleanField(default=False)
    name = models.CharField(max_length=256)
    icon = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=512)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}. {self.name}"
    
    def add_instruction(self, instruction_type_name):
        from instruction.models.instruction import Instruction, InstructionType
        instruction = Instruction.objects.create(type=InstructionType.objects.get(name=instruction_type_name), project=self)
        instruction.save()