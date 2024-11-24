
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Главная страница, показывающая родительские категории
def category_list(request):
    categories = Category.objects.filter(parent__isnull=True)  # Родительские категории
    return render(request, 'shop/category_list.html', {'categories': categories})


# Страница подкатегорий
def subcategory_list(request, parent_id):
    parent_category = get_object_or_404(Category, id=parent_id)
    subcategories = parent_category.subcategories.all()  # Подкатегории этой категории
    return render(request, 'shop/subcategory_list.html', {'parent': parent_category, 'subcategories': subcategories})


def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {'category': category, 'products': products})


# Страница продукта
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})







