from django.contrib import admin
from .models import (UserProfile, Follow, City,
                     HashTag, Post, PostContent,
                     PostLike, Review, ReviewLike)

class PostContentInline(admin.TabularInline):
    model = PostContent
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostContentInline]



admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(City)
admin.site.register(HashTag)
admin.site.register(PostLike)
admin.site.register(Review)
admin.site.register(ReviewLike)