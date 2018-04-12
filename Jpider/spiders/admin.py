from django.contrib import admin
from .models import Author,Article,Tag,Comment
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','body']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name','born_date','born_location']

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id','article_id','pub_date','content')

admin.site.register(Article,ArticleAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment,CommentAdmin)