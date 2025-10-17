from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("用户信息")


def list(request):
    return HttpResponse("用户列表")
