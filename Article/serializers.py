from rest_framework import serializers
from .models import Article, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'parent', 'like_count', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
