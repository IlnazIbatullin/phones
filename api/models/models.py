from tastypie.resources import ModelResource
from shop.models import Category, Brand, Product
from tastypie.authorization import Authorization
from api.authentification import CustomAuthentification
from tastypie.fields import ToManyField


class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'products'
        allowed_methods = ['get', 'post', 'delete']
        authentification = CustomAuthentification()
        authorization = Authorization()
        filtering = {
            'brand': ['exact'],           # Фильтр по бренду
            'price': ['gte', 'lte'],       # Фильтры по цене
            'category': ['exact'],         # Фильтр по категории
        }

    def build_filters(self, filters=None, ignore_bad_filters=False):
        if filters is None:
            filters = {}

        # Отладка входных фильтров
        print("Полученные фильтры в build_filters:", filters)

        orm_filters = super(ProductResource, self).build_filters(filters)

        # Фильтр по категории
        if 'category' in filters:
            orm_filters['category_id'] = filters['category']

        # Фильтры по цене (price_min и price_max)
        if 'price_min' in filters:
            orm_filters['price__gte'] = filters['price_min']
        if 'price_max' in filters:
            orm_filters['price__lte'] = filters['price_max']

        # Обработка JSON-поля specifications
        for key, value in filters.items():
            if key.startswith("spec_"):
                spec_key = key.split("spec_")[1]
                orm_filters[f"specifications__{spec_key}"] = value

        # Отладка конечных фильтров ORM
        print("ORM фильтры после обработки:", orm_filters)

        return orm_filters

    def hydrate(self, bundle):
        bundle.obj.category_id = bundle.data['category_id']
        bundle.obj.brand_id = bundle.data['brand_id']
        return bundle

    def dehydrate(self, bundle):
        bundle.data['category_id'] = bundle.obj.category_id
        bundle.data['brand_id'] = bundle.obj.brand_id
        return bundle



class BrandResource(ModelResource):
    class Meta:
        queryset = Brand.objects.all()
        resource_name = 'brands'
        allowed_methods = ['get', 'post']
        authentification = CustomAuthentification()
        authorization = Authorization()




