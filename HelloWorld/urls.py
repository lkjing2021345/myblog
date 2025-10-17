from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views  # 只保留这一行导入

urlpatterns = [
    path('index/', views.index, name='index'),
    path('redirectTo', RedirectView.as_view(url='/index'), name='redirectTo'),
    path('blog/<int:id>/', views.blog, name='blog'),  # 正确的路由语法
    path('blog2/<int:year>/<int:month>/<int:day>/<int:id>/', views.blog2, name='blog2'),
    re_path(r'^blog3/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.blog3, name='blog3'),
]
