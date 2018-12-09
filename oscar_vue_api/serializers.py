from oscar.core.loading import get_class

from rest_framework import serializers

from oscarapi.serializers import checkout, product


Selector = get_class('partner.strategy', 'Selector')


class MyProductLinkSerializer(product.ProductLinkSerializer):
    images = product.ProductImageSerializer(many=True, required=False)
    price = serializers.SerializerMethodField()
    name = serializers.CharField(source='title')
    created_at = serializers.DateTimeField(source='date_created')
    updated_at = serializers.DateTimeField(source='date_updated')

    class Meta(product.ProductLinkSerializer.Meta):
        fields = ('url', 'id', 'name', 'images', 'price', 'created_at', 'updated_at')

    def get_price(self, obj):
        request = self.context.get("request")
        strategy = Selector().strategy(
            request=request, user=request.user)

        ser = checkout.PriceSerializer(
            strategy.fetch_for_product(obj).price,
            context={'request': request})

        return ser.data
