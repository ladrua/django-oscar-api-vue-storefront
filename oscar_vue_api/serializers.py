from oscar.core.loading import get_class

from rest_framework import serializers

from oscarapi.serializers import checkout, product


Selector = get_class('partner.strategy', 'Selector')

class BasketItemSerializer(serializers.Serializer):
    sku = serializers.CharField(source='product.sku')
    qty = serializers.IntegerField(source='quantity')
    item_id = serializers.IntegerField(source='id')
    
    class Meta:
        fields = '__all__'
        
class WrapperBasketItemSerializer(serializers.Serializer):
    cartItem = serializers.SerializerMethodField()

    def get_cartItem(self, obj):
        sub_data = SubSerializer(obj)
        return sub_data.data
        
    class Meta:
        fields = '__all__'

class BasketUpdateResponseSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    sku = serializers.CharField()
    qty = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField()
    product_type = serializers.CharField(default="simple")
    quote_id = serializers.IntegerField()

    class Meta:
        fields = '__all_'


class UserSerializer(serializers.Serializer):

    group_id = serializers.ReadOnlyField(default=1)
    created_at = serializers.DateTimeField(source='date_joined')
    updated_at = serializers.DateTimeField(source='date_joined')
    created_in =serializers.ReadOnlyField(default="Default")
    email = serializers.EmailField()
    firstname = serializers.CharField(source='first_name')
    lastname = serializers.CharField(source='last_name')
    
    class Meta():
        fields = (
            'id',
            'group_id',
            'created_at',
            'updated_at',
            'created_in',
            'email',
            'firstname',
            'lastname',
        )

class MyProductLinkSerializer(product.ProductLinkSerializer):
    images = product.ProductImageSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()
    name = serializers.CharField(source='title')
    created_at = serializers.DateTimeField(source='date_created')
    updated_at = serializers.DateTimeField(source='date_updated')
    has_options = serializers.ReadOnlyField(default=0)
    type_id = serializers.ReadOnlyField(default="simple")
    
    class Meta(product.ProductLinkSerializer.Meta):
        fields = (
            'id',
            'name',
            'images',
            'price',
            'created_at',
            'updated_at',
            'description',
            'sku',
            'has_options',
            'type_id'
        )

    def get_price(self, obj):
        request = self.context.get("request")
        strategy = Selector().strategy(
            request=request, user=request.user)

        ser = checkout.PriceSerializer(
            strategy.fetch_for_product(obj).price,
            context={'request': request})

        return float(ser.data['incl_tax'])
