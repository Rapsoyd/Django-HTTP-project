from django.contrib import admin
from legend_blog.models import Post, PostReaction, PostComment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff", "is_superuser")
    list_display_links = ("id", "username")


admin.site.register(Post)


@admin.register(PostReaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "reaction")


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("nickname", "post", "body")
