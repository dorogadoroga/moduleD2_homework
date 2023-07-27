from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(UserCategory)


class CategoryAdmin(admin.ModelAdmin):
    # list_display = ("firstname", "lastname", "joined_date",)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)