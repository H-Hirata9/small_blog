from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from knowledge.models import Article, Comment, Profile, DepartmentCode, Belongs
from .serializers import (ArticleSerializer, ReadArticleSerializer, CommentSerializer,
                          ProfileSerializer, DepartmentCodeSerializer, BelongsSerializer)
# Create your views here.




class ProfileViewSet(viewsets.ModelViewSet):
     queryset = Profile.objects.all()
     serializer_class = ProfileSerializer

     def perform_create(self, serializer):
          serializer.save(user=self.request.user)


class MyProfileListView(generics.ListAPIView):
     queryset = Profile.objects.all()
     serializer_class = ProfileSerializer

     def get_queryset(self):
          return self.queryset.filter(user=self.request.user)


class DepartmentCodeViewSet(viewsets.ModelViewSet):
     queryset = DepartmentCode.objects.all()
     serializer_class = DepartmentCodeSerializer

     def perform_create(self, serializer):
          serializer.save(updated_by=self.request.user)


class BelongsViewSet(viewsets.ModelViewSet):
     queryset = Belongs.objects.all()
     serializer_class = BelongsSerializer


class ArticleViewSet(viewsets.ModelViewSet):
     # For author
     queryset = Article.objects.all()
     serializer_class = ArticleSerializer
     read_serializer_class = ReadArticleSerializer
     permission_classes = (IsAuthenticatedOrReadOnly, )

     def get_serializer_class(self):
          if self.request.method.lower() == "get":
               return self.read_serializer_class
          return self.serializer_class

     def perform_create(self, serializer):
          serializer.save(author=self.request.user)

class ReadOnlyArticleViewSet(viewsets.ReadOnlyModelViewSet):
     # For reader
     queryset = Article.objects.filter(is_published=True)
     serializer_class = ReadArticleSerializer
     permission_classes = (IsAuthenticatedOrReadOnly, )


class CommentViewSet(viewsets.ModelViewSet):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer
     permission_classes = (IsAuthenticatedOrReadOnly, )


     def perform_create(self, serializer):
          serializer.save(commenter=self.request.user)

