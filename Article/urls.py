from django.urls import path, include
from . import views  # 导入当前应用的视图
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

# router = DefaultRouter()
# router.register('article', ArticleViewSet)

# 设置应用的命名空间，便于在模板中区分不同应用的URL
app_name = 'Article'

urlpatterns = [
    # 文章列表页：当访问 'article/' 时，调用 article_list 视图
    path('api/login/', views.login_user, name='login'),
    path('', views.article_list, name='article_list'),
    # 文章详情页：URL模式中包含文章ID，如 'article/1/'
    path('<int:id>/', views.article_detail, name='article_detail'),
    path('comments/<int:article_id>/create/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_id>/like/', views.comment_like, name='comment_like'),
    path('api/', views.articles_api, name='articles_api'),
    path('api/register/', views.register_user, name='register'),
    path('api/logout/', views.user_logout, name='logout'),
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('api/get_csrf_token/', views.get_csrf, name='get_csrf'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
    path('explorer/', views.article_explorer, name='article_explorer'),
]
