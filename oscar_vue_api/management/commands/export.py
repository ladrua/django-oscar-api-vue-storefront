from django.core.management.base import BaseCommand, CommandError
from oscar_vue_api import search

class Command(BaseCommand):
    help = "Export products to ElasticSearch"

    def handle(self, *args, **kwargs):
        bulk = search.bulk_indexing()
        self.stdout.write("Just finished indexing")
