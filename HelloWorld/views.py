from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return redirect('/blog/2')

    # content_value = {'msg': "Ciallo～(∠・ω< )⌒★"}
    # return render(request, 'index.html', context=content_value)


# return JsonResponse({'hello': 'world'})


# html = "<font color = 'red'>你好\(@^0^@)/</font>"
# return HttpResponse(html)

# print('页面请求处理中')


def blog(request, id):
    if id == 0:
        return redirect("/static/error.html")
    else:
        return HttpResponse('id是' + str(id) + '的博客页面')


def blog2(request, id, year, month, day):
    return HttpResponse(str(year) + '/' + str(month) + '/' + str(day) + '/' + 'id是' + str(id) + '的博客页面')


def blog3(request, year, month, day):
    return HttpResponse(str(year) + '/' + str(month) + '/' + str(day) + '/')
