from django.contrib import admin
from .models import Brand, Category, Product

admin.site.site_header = "Online shops Admin"
admin.site.site_title = "My shops"
admin.site.index_title = "Welcome to the online shops area"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price')


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductsInline(admin.TabularInline):
    model = Product
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Dates', {
            'fields': ['parent'],
            'classes': ['collapse']
        })
    ]
    inlines = [ProductsInline]


# Регистрируем модели с соответствующими классами администратора
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
