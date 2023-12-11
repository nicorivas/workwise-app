import logging

from django import template

from instruction.models import InstructionElementAgentCall

register = template.Library()

@register.filter
def keyvalue(dict, key):    
    try:
        return dict[str(key)]
    except KeyError:
        return ''

@register.filter
def filter_instruction_step(elements, step):
    elements = elements.filter(step=step)
    return elements

@register.filter
def cast_element(element):
    if element.type.name == "ACA":
        element.__class__ = InstructionElementAgentCall
    return element

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)