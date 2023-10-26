from django.shortcuts import render
from django.template import Template, Context
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def getTemplate(dir, context):
    with open( os.path.join(BASE_DIR, dir)) as templates:
        template = Template(templates.read())
    return template.render(context)