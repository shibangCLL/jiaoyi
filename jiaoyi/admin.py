from django.contrib import admin
from .models import Product, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'price', 'description', 'category', 'author']


admin.site.register(Product, PostAdmin)
admin.site.register(Category)
