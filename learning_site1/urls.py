"""
URL configuration for learning_site1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include, re_path
from django.views.static import serve

# from pathlib import Path
# import sys
#
# root = Path(__file__).parent.parent
# sys.path.append(str(root))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('HelloWorld.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('order/', include(('order.urls', 'order'), namespace='order')),
    path('Article/', include('Article.urls')),
    path('accounts/login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
]
