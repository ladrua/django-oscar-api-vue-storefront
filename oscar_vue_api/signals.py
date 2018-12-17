from django.db.models.signals import post_save
from django.dispatch import receiver
from oscar.core.loading import get_model

from .search import obj_indexing_product

ProductModel = get_model('catalogue', 'product')

@receiver(post_save, sender=ProductModel)
def index_post(sender, instance, **kwargs):
    obj_indexing_product(instance)
