from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Category, Article
from django.contrib.auth.models import User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', ]
    search_fields = ['username', 'email']


admin.site.register(Category)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'created', 'updated']
    search_fields = ['title', 'author__username', 'author__email']

    # 重写方法设置只读字段
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['created', 'updated']
        else:
            return ['created', 'updated', 'title', 'author', 'category']


# 设置网站标题和应用标题
admin.site.site_title = '念舟的学习网站后台管理'
admin.site.index_title = '文章管理模块'
admin.site.site_header = '念舟的网站后台管理系统'
