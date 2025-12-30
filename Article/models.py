from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField('分类名称', max_length=100, unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField('标签名称', max_length=50, unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class Article(models.Model):
    """
    文章模型
    """
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'

    STATUS_CHOICES = [
        (STATUS_DRAFT, '草稿'),
        (STATUS_PUBLISHED, '已发布'),
    ]

    title = models.CharField('文章标题', max_length=70)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='所属分类')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name='作者',
    )
    body = models.TextField('文章正文')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='标签')
    status = models.CharField('文章状态', max_length=20, choices=STATUS_CHOICES, default=STATUS_PUBLISHED)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='评论作者',
    )
    content = models.TextField('评论内容')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='父评论',
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comments',
        blank=True,
        verbose_name='点赞用户',
    )
    is_approved = models.BooleanField('是否审核通过', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} - {self.content[:20]}"

    @property
    def like_count(self):
        return self.likes.count()
