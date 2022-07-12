
from django.contrib.auth import get_user_model
from rest_framework import serializers


from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


from knowledge.models import Article, Comment, DepartmentCode, Profile, Belongs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id',  'email','employee_id','password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class DepartmentCodeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = DepartmentCode
        fields = ('id','department_code','name', 'created_at', 'updated_at',
                  'is_active', 'updated_by',)
        extra_kwargs = {
            'updated_by': {'read_only': True},
        }


class BelongsSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Belongs
        fields = ('id', 'department', 'profile', 'is_primary', 'start_date', 'end_date',)

class ProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Profile
        fields = ('department', 'user', 'created_at', 'free_text')
        extra_kwargs = {
            'user': {'read_only': True},
            'department': {'read_only': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    def validate_article(self, value):
        """
        Check that the blog post is about Django.
        """
        if not value.allow_comment:
            raise serializers.ValidationError("The article author does NOT accept any comment currently.")
        return value
    class Meta:
        model = Comment
        fields = ('id', 'commenter', 'article' , 'ancestor', 'created_at', 'like', 'text')
        extra_kwargs = {
            "commenter" : {"read_only": True},
        }


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
        fields = ('id', 'title', 'text', 'author', 'tags', 'article_images', 'created_at',
                  'updated_at', 'is_published', 'initial_published_at', 'last_published_at',
                  'comments', 'like', 'allow_comment', )
        extra_kwargs = {
            "author" : {"read_only": True}
        }


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    initial_published_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    last_published_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'author', 'tags','article_images','created_at',
                  'updated_at', 'is_published','initial_published_at','last_published_at',
                   'like', 'allow_comment',)
        extra_kwargs = {
            "author" : {"read_only": True},
        }

