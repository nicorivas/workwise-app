from django.db import models

from actions.models import Action

class InstructionType(models.Model):
    """An InstructionType is a step of an Action. It is a container of InstructionElements, and it's main function is to stablish dependencies of flow in the action.

    Attributes:
        name (str): The name of the instruction.
        description (str): The description of the instruction.
        action (Action): The action that this instruction belongs to.
        previous_instruction (Instruction): The previous instruction that this instruction depends on.
    """
    index = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    description = models.TextField(default="", null=True, blank=True)
    flow_visible = models.BooleanField(default=False)
    flow_title = models.CharField(max_length=255, default="", null=True, blank=True)
    flow_description = models.TextField(default="", null=True, blank=True)
    previous_instruction = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    step = models.IntegerField(choices=[(0,"Write"),(1,"Revise"),(2,"Modify")], default=0)
    style = models.CharField(max_length=64, choices=[
        ("normal","normal")
        ,("seamless","seamless")
        ,("flow","flow")
        ], default="normal")

    def __str__(self):
        return f"Instruction Type {self.pk}: {self.name}"
    
    def get_possible_actions(self):
        if self.previous_instruction:
            return self.previous_instruction.action.get_next_actions()
        else:
            return Action.objects.filter(previous_action=None)