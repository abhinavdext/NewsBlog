from django.contrib import admin

from .models import Article, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    search_fields = (
        'name',
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'author',
        'category',
        'status',
        'views',
        'created_at',
        'published_at',
    )

    list_filter = (
        'status',
        'category',
        'created_at',
    )

    search_fields = (
        'title',
        'content',
        'author__username',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    readonly_fields = (
        'views',
        'created_at',
        'updated_at',
    )

    ordering = (
        '-created_at',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'article',
        'content',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'content',
        'user__username',
        'article__title',
    )

    ordering = (
        '-created_at',
    )