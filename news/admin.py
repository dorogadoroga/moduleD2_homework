from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating')
    list_filter = ('author', 'rating')
    search_fields = ('author',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'title', 'rating')
    list_filter = ('author', 'date', 'rating', 'category')
    search_fields = ('author', 'date', 'title', 'category')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'rating')
    list_filter = ('author', 'post', 'rating')
    search_fields = ('author', 'post')

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    list_filter = ('post', 'category')
    search_fields = ('post', 'category')

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ('user', 'category')
    search_fields = ('user', 'category')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)