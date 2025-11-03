from django.db import models


# class Category(models.Model):
#     name = models.CharField('分类名称', max_length=100, unique=True)
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#
#     class Meta:
#         verbose_name = '文章分类'
#         verbose_name_plural = verbose_name  # 避免Admin后台显示英文复数
#
#     # def __init__(self, *args: any, **kwargs: any):
#     #     super().__init__(*args, **kwargs)
#     #     self.article_count = None
#     #
#     # def __init__(self, *args: Any, **kwargs: Any):
#     #     super().__init__(args, kwargs)
#     #     self.article_set = None
#
#     @property
#     def article_count(self):
#         """作为属性而不是在__init__中设置"""
#         if hasattr(self, '_article_count'):
#             return self._article_count
#         self._article_count = self.article_set.count()
#         return self._article_count
#
#     def __str__(self):
#         def __str__(self):
#             # 🔥 修复：简化返回逻辑
#             return str(self.name)  # 用于在Admin后台或Shell中直观显示

class Category(models.Model):
    name = models.CharField('分类名称', max_length=100, unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 绝对确保返回字符串
        try:
            return f"{self.name}"
        except:
            return "Category Object"


class Article(models.Model):
    """
    文章模型
    """
    title = models.CharField('文章标题', max_length=70)
    # 关键：使用外键关联分类。on_delete=models.CASCADE表示分类删除时，该分类下所有文章也被删除。
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='所属分类')
    author = models.CharField('作者', max_length=100)
    body = models.TextField('文章正文')
    created = models.DateTimeField('创建时间', auto_now_add=True)  # 自动设置为文章创建的时间
    updated = models.DateTimeField('更新时间', auto_now=True)  # 每次保存对象时自动更新为当前时间

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.title)
