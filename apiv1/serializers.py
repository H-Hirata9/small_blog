
from django.contrib.auth import get_user_model
from rest_framework import serializers


from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


from knowledge.models import Article, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id',  'email','employee_id',)


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"

class ReadArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True)
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    initial_published_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    last_published_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author', 'tags','article_images','created_at',
                  'updated_at', 'is_published','initial_published_at','last_published_at',
                  'comments')

class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    initial_published_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    last_published_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author', 'tags','article_images','created_at',
                  'updated_at', 'is_published','initial_published_at','last_published_at')

