from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Мои заметки</h1><p>Скоро здесь появится список.</p>")

