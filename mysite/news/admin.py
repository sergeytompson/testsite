from django.contrib import admin
from .models import News, Category, Comments


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'created_at', 'updated_at', 'is_publish']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'content']
    list_editable = ['is_publish']
    list_filter = ['category', 'is_publish']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'text', 'created_at', 'news']
    search_fields = ['username', 'text', 'news']
    list_filter = ['username']


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
