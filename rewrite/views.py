from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.db import models
from django.template.defaulttags import comment
from generate import Generate


class reply_generate(generate.Generate):

