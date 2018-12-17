from django.conf.urls import url
from oscarapi.app import RESTApiApplication
from oscar_vue_api.authtoken import obtain_auth_token
from . import views

class MyRESTApiApplication(RESTApiApplication):

    def get_urls(self):
        urls = [
            url(r'^user/login', obtain_auth_token),
            url(r'^user/me', views.CurrentUserView.as_view()),
            url(r'^cart/create', views.CreateBasketView.as_view()),
            url(r'^cart/pull', views.PullBasketView.as_view()),
            url(r'^cart/update', views.UpdateBasketItemView.as_view()),
            url(r'^cart/delete', views.DeleteBasketItemView.as_view()),
            url(r'^cart/totals', views.BasketTotalsView.as_view()),
            url(r'^cart/shipping-information', views.BasketTotalsView.as_view()),
            #url(r'^products/index', views.ProductList.as_view(), name='product-list'),
            url(r'^catalog', views.ElasticView.as_view()),
        ]
        return urls + super(MyRESTApiApplication, self).get_urls()

application = MyRESTApiApplication()
