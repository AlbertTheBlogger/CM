from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from search import *

# Create your views here.

def get_comment(request):
    if request.methond == 'GET':
