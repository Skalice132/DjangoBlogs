from django.contrib import admin
from .models import Post,Tag


admin.site.register(Tag)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','text','date','author')
    list_display_links = ('title',)
    search_fields = ('title','text')

admin.site.register(Post, PostAdmin)
