from django.http import HttpResponse
# from django.shortcuts import render


def index(request):
    return HttpResponse('index page')


def hello(request):
    return HttpResponse('Hello, Dima')
