from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, resolve


# Create your views here.
def index(request):
    route_url = reverse('order:index')
    print("reverse反向解析的路由地址", route_url)
    result = resolve(route_url)
    print("resolve通过路由地址得到路由信息", str(result))
    return HttpResponse("订单信息")


def list(request, year, month, day):
    kwargs = {'year': year, 'month': month, 'day': day}
    route_url = reverse('order:list', kwargs=kwargs)
    print("reverse反向解析的路由地址", route_url)
    result = resolve(route_url)
    print("resolve通过路由地址得到路由信息", str(result))
    return HttpResponse("订单列表")
