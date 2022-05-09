from django.contrib import admin

from .models import Post, Group, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    search_fields = ('text',)
    list_editable = ('group',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'description',
    )
    search_fields = ('title', 'description')
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'created',
    )
    search_fields = ('text',)
    list_filter = ('created',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author'
    )
    empty_value_display = '-пусто-'
