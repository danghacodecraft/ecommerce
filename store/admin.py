from django.contrib import admin
from .models import Category, SubCategory, Product, Contact


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category', 'image', 'slug']


admin.site.register(Category)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product)
admin.site.register(Contact)