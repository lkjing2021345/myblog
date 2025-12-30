from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .models import Article, Category, Tag, Comment
from rest_framework import viewsets
from .serializers import ArticleSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import logout


# Create your views here.

def user_login(request):
    return render(request, 'auth/login.html')


def user_register(request):
    return render(request, 'auth/register.html')


@login_required
def articles_api(request):
    """
    处理文章列表展示和搜索功能
    """
    # 从请求中获取搜索关键词和排序参数
    search_query = request.GET.get('q', '').strip()  # 'q' 是搜索框的名称
    order = request.GET.get('order', '-created')  # 默认按创建时间倒序（最新）

    # 基础查询集：所有已发布的文章，并使用select_related优化外键查询[3](@ref)
    # 假设你的Article模型有一个`is_published`字段，若没有可先去掉这个filter
    articles = Article.objects.select_related('category')  # 预加载分类信息，避免N+1问题

    # 搜索逻辑：如果用户输入了搜索词
    if search_query:
        # 使用Q对象进行联合搜索，在标题和正文中查找[3,4](@ref)
        articles = articles.filter(
            Q(title__icontains=search_query) |  # 标题中包含，不区分大小写
            Q(body__icontains=search_query)  # 正文中包含，不区分大小写
        )

    # 排序逻辑
    articles = articles.order_by(order)

    # 准备传递给模板的上下文
    context = {
        'articles': articles,
        'search_query': search_query,  # 将搜索词传回模板，方便显示和保留在输入框
        'order': order,
    }
    return render(request, 'article/list.html', {'articles': articles})


def login_page(request):
    """处理GET请求，返回注册页面"""
    if request.method == 'GET':
        return render(request, 'auth/login.html')  # 确保模板路径正确
    # 对于非GET请求，可以返回错误或重定向，但通常注册页面只处理GET
    from django.http import HttpResponseNotAllowed
    return HttpResponseNotAllowed(['GET'])


@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # 关键：明确只使用 Token 认证
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    用户注销，删除其认证 Token。
    """
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
        logout(request)  # 如果同时使用了会话，可清理 session
        return Response({"detail": "成功退出登录。"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "用户未登录。"}, status=status.HTTP_400_BAD_REQUEST)


def logout_page(request):
    """处理GET请求，返回注册页面"""
    if request.method == 'GET':
        return render(request, 'auth/logout.html')  # 确保模板路径正确
    # 对于非GET请求，可以返回错误或重定向，但通常注册页面只处理GET
    from django.http import HttpResponseNotAllowed
    return HttpResponseNotAllowed(['GET'])


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method != 'POST':
        # 对于非POST请求直接返回JSON错误
        return JsonResponse({'error': '只接受POST请求'}, status=405)
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key, 'message': '登录成功'})
    else:
        return JsonResponse({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)


def register_page(request):
    """处理GET请求，返回注册页面"""
    if request.method == 'GET':
        return render(request, 'auth/register.html')  # 确保模板路径正确
    # 对于非GET请求，可以返回错误或重定向，但通常注册页面只处理GET
    from django.http import HttpResponseNotAllowed
    return HttpResponseNotAllowed(['GET'])


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': '用户名和密码为必填项'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    # 注册成功后自动登录，为其创建并返回Token
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'message': '用户注册成功'}, status=status.HTTP_201_CREATED)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


def article_list(request):
    search_query = request.GET.get('q', '').strip()
    tag_filter = request.GET.get('tag', '').strip()
    category_filter = request.GET.get('category', '').strip()
    order = request.GET.get('order', '-created')

    allowed_orders = {'created', '-created', 'title', '-title'}
    if order not in allowed_orders:
        order = '-created'

    articles = (
        Article.objects.select_related('category', 'author')
        .prefetch_related('tags')
        .filter(status=Article.STATUS_PUBLISHED)
    )

    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query)
            | Q(body__icontains=search_query)
            | Q(tags__name__icontains=search_query)
        )

    if tag_filter:
        articles = articles.filter(tags__name=tag_filter)

    if category_filter:
        articles = articles.filter(category_id=category_filter)

    articles = articles.order_by(order).distinct()
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'tag_filter': tag_filter,
        'category_filter': category_filter,
        'order': order,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = get_object_or_404(Article.objects.select_related('author', 'category'), id=id)
    replies = Comment.objects.filter(is_approved=True).select_related('author')
    comments = (
        Comment.objects.filter(article=article, is_approved=True, parent__isnull=True)
        .select_related('author')
        .prefetch_related(Prefetch('replies', queryset=replies), 'likes')
    )
    return render(
        request,
        'article/details.html',
        {
            'article': article,
            'comments': comments,
        },
    )


@login_required
def comment_create(request, article_id):
    if request.method != 'POST':
        return JsonResponse({'error': '只接受POST请求'}, status=405)

    article = get_object_or_404(Article, id=article_id)
    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_id')

    if not content:
        return JsonResponse({'error': '评论内容不能为空'}, status=400)

    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id, article=article)

    Comment.objects.create(
        article=article,
        author=request.user,
        content=content,
        parent=parent,
    )
    return JsonResponse({'message': '评论已提交，等待审核或展示。'})


@login_required
def comment_like(request, comment_id):
    if request.method != 'POST':
        return JsonResponse({'error': '只接受POST请求'}, status=405)

    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': comment.like_count})


def get_csrf(request):
    # 调用csrf上下文处理器，生成包含CSRF令牌的字典
    x = csrf(request)  # x是一个字典，包含{'csrf_token': '加密的令牌值'}

    # 从字典中取出具体的CSRF令牌值
    csrf_token = x['csrf_token']  # 此时csrf_token变量包含实际的令牌字符串

    # 将令牌返回给前端（这里示例代码有误，应只返回令牌本身）
    return HttpResponse(csrf_token)  # 应直接返回令牌，而非拼接无关内容


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_data(request, avg_daily=None):
    # """提供仪表盘所需的JSON数据"""
    # if not request.user.is_authenticated:
    #     return JsonResponse({'error': '认证失败'}, status=401)

    # 基础统计
    total_articles = Article.objects.count()
    total_categories = Category.objects.count()

    # 近期发布趋势（过去30天）
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_articles = Article.objects.filter(created__gte=thirty_days_ago)

    # 按日期统计发布数量
    date_counts = recent_articles.extra(
        {'date': "date(created)"}
    ).values('date').annotate(count=Count('id')).order_by('date')

    # 分类文章数量统计
    category_stats = Category.objects.annotate(article_count=Count('article'))
    category_data = []

    for cat in category_stats:
        # 检查分类名称是否存在，如果为空则使用备用名称
        category_name = cat.name
        if not category_name or category_name.strip() == "":
            category_name = f"分类-{cat.id}"  # 使用分类ID作为备用名称

        category_data.append({
            'name': category_name,  # 使用处理后的名称
            'count': cat.article_count
        })

    data = {
        'overview': {
            'total_articles': total_articles,
            'total_categories': total_categories,
            'avg_daily_posts': avg_daily
        },
        'trend_data': list(date_counts),
        'category_data': category_data
    }

    return JsonResponse(data)


def dashboard_view(request):
    """渲染仪表盘页面"""
    return render(request, 'article/dashboard.html')


def article_explorer(request):
    """交互式文章探索页面"""
    # 获取所有分类用于过滤器
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # 获取搜索参数
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    tag_filter = request.GET.get('tag', '')

    articles = Article.objects.select_related('category').prefetch_related('tags')

    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(body__icontains=search_query)
        )

    if category_filter:
        articles = articles.filter(category_id=category_filter)

    if tag_filter:
        articles = articles.filter(tags__name=tag_filter)

    context = {
        'articles': articles,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
        'tags': tags,
        'selected_tag': tag_filter,
    }
    return render(request, 'article/explorer.html', context)
