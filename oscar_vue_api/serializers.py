from oscar.core.loading import get_class

from rest_framework import serializers

from oscarapi.serializers import checkout, product


Selector = get_class('partner.strategy', 'Selector')

class TotalSegmentSerializer(serializers.Serializer):
    code = serializers.CharField()
    title = serializers.CharField()
    value = serializers.DecimalField(decimal_places=2, max_digits=12)
    
    class Meta:
        fields = '__all__'
        
class FullBasketItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(source='id')
    price = serializers.IntegerField(source='price_incl_tax')
    base_price = serializers.IntegerField(source='price_excl_tax')
    qty = serializers.IntegerField(source='quantity')
    row_total = serializers.IntegerField(source='price_incl_tax')
    base_row_total = serializers.IntegerField(source='price_excl_tax')
    row_total_with_discount = serializers.IntegerField(source='price_incl_tax')
    tax_amount = serializers.IntegerField(default=0)
    base_tax_amount = serializers.IntegerField(default=0)
    tax_percent = serializers.IntegerField(default=0)
    discount_amount = serializers.IntegerField(default=0)
    base_discount_amount = serializers.IntegerField(default=0)
    discount_percent = serializers.IntegerField(default=0)
    options = serializers.ListField(default=None)
    wee_tax_applied_amount = serializers.IntegerField(default=0)
    wee_tax_applied = serializers.IntegerField(default=0)
    name = serializers.CharField(source='product.title')
    product_option = serializers.ListField(default=None)

    class Meta:
        fields = '__all__'
    
    

class FullBasketSerializer(serializers.Serializer):
    grand_total = serializers.IntegerField(source='total_incl_tax_excl_discounts')
    weee_tax_applied_amount = serializers.IntegerField(default=0)
    base_currency_code = serializers.CharField(source='currency')
    quote_currency_code = serializers.CharField(source='currency')
    items_qty = serializers.IntegerField(source='num_items')
    items = FullBasketItemSerializer(many=True, source='lines')
    total_segments = serializers.SerializerMethodField()

    def get_total_segments(self, obj):
        segments = TotalSegmentSerializer(many=True, data=self.context['total_segments'])
        segments.is_valid()
        return segments.data
    class Meta:
        fields = '__all__'
    

class BasketItemSerializer(serializers.Serializer):
    sku = serializers.CharField(source='product.upc')
    qty = serializers.IntegerField(source='quantity')
    item_id = serializers.IntegerField(source='id')
    price = serializers.IntegerField(source='price_incl_tax')
    name = serializers.CharField(source='product.title')
    product_type = serializers.CharField(default='simple')
    quote_id = serializers.CharField(source='basket.id')
    product_option = serializers.DictField(default={})
    
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
