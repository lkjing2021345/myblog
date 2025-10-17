from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Article
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
    articles = Article.objects.all().order_by('-created')
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
    articles = Article.objects.all().order_by('-created')
    return render(request, 'article/list.html', {'articles': articles})


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'article/details.html', {'article': article})


def get_csrf(request):
    # 调用csrf上下文处理器，生成包含CSRF令牌的字典
    x = csrf(request)  # x是一个字典，包含{'csrf_token': '加密的令牌值'}

    # 从字典中取出具体的CSRF令牌值
    csrf_token = x['csrf_token']  # 此时csrf_token变量包含实际的令牌字符串

    # 将令牌返回给前端（这里示例代码有误，应只返回令牌本身）
    return HttpResponse(csrf_token)  # 应直接返回令牌，而非拼接无关内容
