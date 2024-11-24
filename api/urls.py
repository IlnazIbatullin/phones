from api.models.models import ProductResource, BrandResource
from api.models.category_resource import CategoryResource
from tastypie.api import Api
from django.urls import path, include


api = Api(api_name='v1')
category_resource = CategoryResource()
product_resource = ProductResource()
brand_resource = BrandResource()
api.register(category_resource)
api.register(product_resource)
api.register(brand_resource)



urlpatterns = [
    path('', include(api.urls), name='index')
]