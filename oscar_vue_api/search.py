from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Integer, Float, Boolean, Object, Nested
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from oscar.core.loading import get_model, get_class

connections.create_connection(hosts=['elastic:changeme@db.local'], timeout=20)

class ProductsIndex(DocType):

    category_ids = Text()
    type_id = Text()
    sku = Text()
    has_options = Text()
    required_options = Text()
    created_at = Date()
    updated_at = Date()
    status = Integer()
    visibility = Integer()
    tax_class_id = Integer()
    description = Text()
    name = Text()
    image = Text()
    thumbnail = Text()
    media_gallery = Text()
    url_key = Text()
    url_path = Text()
    weight = Float()
    price = Float()
    special_price = Float()
    news_from_date = Date()
    news_to_date = Date()
    special_from_date = Date()
    special_to_date = Date()
    stock_item = Object(properties={'is_in_stock': Boolean()})
    category = Nested(
        properties = {
            'category_id': Integer(),
            'name': Text(),
        }
    )
    stock = Object(properties={'is_in_stock': Boolean()})
    configurable_children = Nested(
        properties = {
            'sku': Text(),
            'price': Float(),
            'image': Text(),
            'is_salable': Boolean(),
            'product_id': Integer(),
        }
    )

    class Index:
        name = 'storefront_catalog'
        doc_type = 'product'

    class Meta:
        doc_type = 'product'


def bulk_indexing_products():
    ProductsIndex().init()
    es = connections.get_connection()
    Product = get_model('catalogue', 'product')
    bulk(client=es, actions=(obj_indexing_product(b) for b in Product.objects.all().iterator()))

def obj_indexing_product(product):
    if product.wimages.first():
        image=product.wimages.first().image.file.path
    else:
        image=""
    all_categories = []
    for category in product.categories.all():
        category_mapping = [{
            'category_id': category.id,
            'name': category.title
        }]
        #all_categories.update(category_mapping)
        all_categories += category_mapping
        
    obj = ProductsIndex(
        meta={
            'id': product.id,
        },
        type_id="simple",
        sku=product.sku,
        name=product.title,
        price=200,
        image=image,
        description=product.description,
        category=all_categories,
    )
    obj.save()
    return obj.to_dict(include_meta=True)


















