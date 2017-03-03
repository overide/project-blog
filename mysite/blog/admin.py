from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
	list_display = ('title','slug','author','publish','status')
	list_filter = ('status','publish','created','author')
	search_fields = ('title','body')
	raw_id_fields = ('author',)
	prepopulated_fields = {'slug':('title',)}
	date_hierarchy = 'publish'
	ordering = ['status','publish']

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name','email','created','body','post','active')
	list_filter = ('created','updated','active')
	search_fields = ('email','post','name')
	raw_id_fields = ('post',)
	date_hierarchy = 'created'
	ordering = ['active','created']

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)