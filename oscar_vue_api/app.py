from django.conf.urls import url
from oscarapi.app import RESTApiApplication
from oscar_vue_api.authtoken import obtain_auth_token
from . import views

class MyRESTApiApplication(RESTApiApplication):

    def get_urls(self):
        urls = [
            url(r'^auth/admin', obtain_auth_token),
            url(r'^products/$', views.ProductList.as_view(), name='product-list'),
        ]
        return urls + super(MyRESTApiApplication, self).get_urls()

application = MyRESTApiApplication()
