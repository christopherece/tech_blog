from django.contrib import admin
from .models import Post
from .models import Category
from .models import Comment


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'content',
        'author',
        'is_published',
        'created_at',
        'updated_at',
    )
    list_editable = ['is_published',]



admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post,PostAdmin)
