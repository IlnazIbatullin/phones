# # api/resources/category_resource.py
# from tastypie.resources import ModelResource
# from shop.models import Category
#
# class CategoryResource(ModelResource):
#     class Meta:
#         queryset = Category.objects.filter(parent=None)
#         resource_name = 'category'
#         allowed_methods = ['get']
#         filtering = {
#             # Задайте фильтры, если нужно
#         }


from tastypie.resources import ModelResource
from tastypie import fields
from shop.models import Category

class CategoryResource(ModelResource):
    subcategories = fields.ToManyField(
        'self',
        attribute='subcategories',
        null=True,
        full=True
    )

    class Meta:
        queryset = Category.objects.filter(parent=None)
        resource_name = 'category'
        list_allowed_methods = ['get']


