from django.shortcuts import render

from oscarapi.views import product, basket

from .serializers import *
from .services import elastic_result
from .renderers import CustomJSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from oscarapi.basket import operations
from rest_framework.renderers import JSONRenderer
from oscar.core.loading import get_model
from rest_framework import status

BasketModel = get_model('basket', 'Basket')
ProductModel = get_model('catalogue', 'Product')
LineModel = get_model('basket', 'Line')

Selector = get_class('partner.strategy', 'Selector')

selector = Selector()

#class ProductList(product.ProductList):
#    serializer_class = MyProductLinkSerializer

class CurrentUserView(APIView):

    renderer_classes = (CustomJSONRenderer, )
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CreateBasketView(APIView):
    """
    Api for retrieving a user's basket id.
    GET:
    Retrieve your basket id.
    """

    renderer_classes = (CustomJSONRenderer, )
    
    def post(self, request, format=None):
        basket = operations.get_basket(request)
        return Response(basket.id)

class PullBasketView(APIView):

    renderer_classes = (CustomJSONRenderer, )
    
    def get(self, request, format=None):
        basket_id = request.query_params.get('cartId')
        basket = BasketModel.objects.filter(pk=basket_id).first()
        serializer = BasketItemSerializer(data=basket.lines, many=True)
        serializer.is_valid()
        print(serializer.data)
        return Response(serializer.data)

class UpdateBasketItemView(APIView):

    renderer_classes = (CustomJSONRenderer, )
    
    def validate(self, basket, product, quantity, options):
        availability = basket.strategy.fetch_for_product(
            product).availability

        # check if product is available at all
        if not availability.is_available_to_buy:
            return False, availability.message

        # check if we can buy this quantity
        allowed, message = availability.is_purchase_permitted(quantity)
        if not allowed:
            return False, message

        # check if there is a limit on amount
        allowed, message = basket.is_quantity_allowed(quantity)
        if not allowed:
            return False, message
        return True, None

    def post(self, request, format=None):
        
        quantity = int(request.data['cartItem']['qty'])
        product_sku = request.data['cartItem']['sku']
        quote_id = request.data['cartItem']['quoteId']
        product = ProductModel.objects.filter(sku=product_sku).first()
        
        if 'item_id' in request.data['cartItem']:
            line_id = request.data['cartItem']['item_id']
            current_line = LineModel.objects.filter(pk=line_id).first()
            current_line.quantity = quantity
            current_line.save()
        else:
            basket_id = request.query_params.get('cartId')
            basket = BasketModel.objects.filter(pk=basket_id).first()
            basket._set_strategy(selector.strategy(request=request, user=request.user))
            basket_valid, message = self.validate(
                basket, product, int(quantity), options=None)
            if not basket_valid:
                return Response(
                    message,
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            line = basket.add_product(product, quantity, options=None)
            line_id = line[0].id
        response_item = {}
        response_item['item_id'] = line_id
        response_item['sku'] = product_sku
        response_item['qty'] = quantity
        response_item['name'] = product.title
        response_item['price'] = 200
        response_item['product_type'] = 'simple'
        response_item['quote_id'] = quote_id
        response = BasketUpdateResponseSerializer(data=response_item)
        response.is_valid()
        print(response.data)
        return Response(response.data)

class DeleteBasketItemView(APIView):
    renderer_classes = (CustomJSONRenderer, )
    
    def post(self, request):
        line_id = request.data['cartItem']['item_id']
        line = LineModel.objects.filter(pk=line_id).first()
        response = line.delete()
        return Response(response)

class BasketTotalsView(APIView):
    renderer_classes = (CustomJSONRenderer, )
    
    def post(self, request, format=None):
        return self.do_it(request)
    
    def get(self, request, format=None):
        return self.do_it(request)
    
    def do_it(self, request, format=None):
        basket_id = request.query_params.get('cartId')
        basket = BasketModel.objects.filter(pk=basket_id).first()
        basket._set_strategy(selector.strategy(request=request, user=request.user))
        total_segments = []
        total_segments.append({ 'code': 'subtotal', 'title': 'Subtotal', 'value': basket.total_excl_tax})
        total_segments.append({ 'code': 'tax', 'title': 'Tax', 'value': basket.total_tax })
        total_segments.append({ 'code': 'grand_total', 'title': 'Grand Total', 'value': basket.total_incl_tax })
        serializer = FullBasketSerializer(basket, context={'total_segments': total_segments})
        return Response(serializer.data)
    
class ElasticView(APIView):
    permission_classes=[]
    renderer_classes = (JSONRenderer, )
    
    def get(self, request, format=None):
        _search = elastic_result(self, request)
        return _search
        pass
    
    def post(self, request):
        _search = elastic_result(self, request)
        return _search
        pass

