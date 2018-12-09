from django.conf.urls import url
from oscarapi.app import RESTApiApplication
from oscar_vue_api.authtoken import obtain_auth_token

class MyRESTApiApplication(RESTApiApplication):

    def get_urls(self):
        urls = [
            url(r'^auth/admin', obtain_auth_token),
        ]
        return urls + super(MyRESTApiApplication, self).get_urls()

application = MyRESTApiApplication()
