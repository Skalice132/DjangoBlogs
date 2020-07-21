from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','text','date','author')
    list_display_links = ('title',)
    search_fields = ('title','text')

admin.site.register(Post, PostAdmin)
