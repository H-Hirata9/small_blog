from django.contrib import admin

from .models import Article, ArticleImage, ArticleAttachedFile, Comment
# Register your models here.


class ArticleImageInline(admin.StackedInline):
    model = ArticleImage

class ArticleAttachedFileInline(admin.StackedInline):
    model = ArticleAttachedFile

class CommentInline(admin.StackedInline):
    model = Comment
    fields = ('commenter', 'text','ancestor',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','author', 'title', 'text', 'created_at', 'updated_at',
                    'is_published', 'tags',)
    ordering = ('-updated_at',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'like', 'follower',
                       'initial_published_at','last_published_at',)
    inlines = (
        ArticleImageInline,
        ArticleAttachedFileInline,
        CommentInline,
    )




admin.site.register(Article,ArticleAdmin)