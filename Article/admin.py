from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Category, Article, Tag, Comment

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'email']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'status', 'created', 'updated']
    search_fields = ['title', 'author__username', 'author__email']
    list_filter = ['status', 'category', 'tags']
    filter_horizontal = ['tags']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['created', 'updated']
        return ['created', 'updated', 'title', 'author', 'category']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'author', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__username']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = '审核通过所选评论'


admin.site.site_title = '念舟的学习网站后台管理'
admin.site.index_title = '文章管理模块'
admin.site.site_header = '念舟的网站后台管理系统'
