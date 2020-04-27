from rest_framework import serializers
from .models import *


class OrderDetailsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'


class TransportDetailsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDetails
        fields = '__all__'


class CustomerDetailsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'


class BillingDetailsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetails
        fields = '__all__'


class OrderDetailsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ('orderId', 'orderItemId', 'orderDate', 'latestDeliveryDate', 'ean', 'title', 'quantity',
                  'offerPrice', 'offerCondition', 'offerReference', 'fulfilmentMethod')


class TransportDetailsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDetails
        fields = ('transportId', 'transporterCode', 'trackAndTrace')


class CustomerDetailsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ('salutationCode', 'zipCode', 'countryCode', 'email')


class BillingDetailsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetails
        fields = ('salutationCode', 'zipCode', 'countryCode', 'email')


class ShippingDetailsListSerializer(serializers.ModelSerializer):
    seller_profile = serializers.SerializerMethodField("get_seller_name")
    orderDetails = OrderDetailsListSerializer(many=True)
    transportDetails = TransportDetailsListSerializer()
    customerDetails = CustomerDetailsListSerializer()
    billingDetails = BillingDetailsListSerializer()


    def get_seller_name(self, instance):
        return instance.seller_profile.seller_name

    class Meta:
        model = ShippingDetails
        fields = ('seller_profile', 'shipmentId', 'shipmentDate', 'shipmentReference', 'pickUpPoint', 'orderDetails',
                  'transportDetails', 'customerDetails', 'billingDetails')