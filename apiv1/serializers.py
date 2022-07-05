
from django.contrib.auth import get_user_model
from rest_framework import serializers

from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


from knowledge.models import Article, MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id',  'email','employee_id',)

class ReadArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    published_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author', 'tags','article_images','created_at',
                  'updated_at', 'published_at',)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    published_at = serializers.BooleanField()


    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author', 'tags','article_images','created_at',
                  'updated_at', 'published_at',)

