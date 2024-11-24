from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:parent_id>/', views.subcategory_list, name='subcategory_list'),
    path('category/<int:category_id>/products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail')

]

