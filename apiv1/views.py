from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from knowledge.models import Article
from .serializers import ArticleSerializer, ReadArticleSerializer
# Create your views here.

class ArticleViewSet(viewsets.ModelViewSet):
     queryset = Article.objects.all()
     serializer_class = ArticleSerializer
     read_serializer_class = ReadArticleSerializer
     permission_classes = (IsAuthenticatedOrReadOnly, )

     def get_serializer_class(self):
          if self.request.method.lower() == "get":
               return self.read_serializer_class
          return self.serializer_class
