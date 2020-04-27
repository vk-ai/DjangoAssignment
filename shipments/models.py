from django.db import models
from seller_profile.models import SellerProfile
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class OrderDetails(models.Model):
    orderId = models.CharField(max_length=150, blank=True, null=True)
    orderItemId = models.CharField(max_length=150, blank=True, null=True)
    orderDate = models.CharField(max_length=200, blank=True, null=True)
    latestDeliveryDate = models.CharField(max_length=200, blank=True, null=True)
    ean = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    offerPrice = models.FloatField(default=0.0)
    offerCondition = models.CharField(max_length=200, blank=True, null=True)
    offerReference = models.CharField(max_length=20, blank=True, null=True)
    fulfilmentMethod = models.CharField(max_length=10, blank=True, null=True)

    # def __str__(self):
    #     return self.orderId or ''


class TransportDetails(models.Model):
    transportId = models.IntegerField(default=0)
    transporterCode = models.CharField(max_length=10, blank=True, null=True)
    trackAndTrace = models.CharField(max_length=50, blank=True, null=True)
    shippingLabelId = models.IntegerField(default=0)
    shippingLabelCode = models.CharField(max_length=50, blank=True, null=True)

    # def __str__(self):
    #     return self.transportId or ''


class CustomerDetails(models.Model):
    pickUpPointName = models.CharField(max_length=250, blank=True, null=True)
    salutationCode = models.CharField(max_length=20, blank=True, null=True)
    firstName = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)
    streetName = models.CharField(max_length=20, blank=True, null=True)
    houseNumber = models.CharField(max_length=20,blank=True, null=True)
    houseNumberExtended = models.CharField(max_length=20, blank=True, null=True)
    addressSupplement = models.CharField(max_length=50, blank=True, null=True)
    extraAddressInformation = models.CharField(max_length=50, blank=True, null=True)
    zipCode = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    countryCode = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(verbose_name=_('email address'),
                              max_length=255,
                              null=True, blank=True)
    vatNumber = models.CharField(max_length=100, blank=True, null=True)
    chamberOfCommerceNumber = models.CharField(max_length=100, blank=True, null=True)
    orderReference = models.CharField(max_length=100, blank=True, null=True)
    deliveryPhoneNumber = models.CharField(_('Contact no'),
                             max_length=13,
                             null=True, blank=True
                             )

    # def __str__(self):
    #     return self.firstName or ''


class BillingDetails(models.Model):
    pickUpPointName = models.CharField(max_length=250, blank=True)
    salutationCode = models.CharField(max_length=20, blank=False)
    firstName = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=20, blank=True)
    streetName = models.CharField(max_length=20, blank=True)
    houseNumber = models.CharField(max_length=20, blank=True)
    houseNumberExtended = models.CharField(max_length=20, blank=True)
    addressSupplement = models.CharField(max_length=50, blank=True)
    extraAddressInformation = models.CharField(max_length=50, blank=True)
    zipCode = models.CharField(max_length=20, blank=False)
    city = models.CharField(max_length=50, blank=True)
    countryCode = models.CharField(max_length=20, blank=False)
    email = models.EmailField(verbose_name=_('email address'),
                              max_length=255,
                              null=True, blank=True)
    vatNumber = models.CharField(max_length=100, blank=True)
    chamberOfCommerceNumber = models.CharField(max_length=100, blank=True)
    orderReference = models.CharField(max_length=100, blank=True)
    deliveryPhoneNumber = models.CharField(_('Contact no'),
                                           max_length=13,
                                           null=True, blank=True
                                           )

    # def __str__(self):
    #     return self.firstName or ''


class ShippingDetails(models.Model):
    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    shipmentId = models.IntegerField(default=0, unique=True)
    shipmentDate = models.CharField(max_length=150, blank=True, null=True)
    shipmentReference = models.CharField(max_length=100, blank=True, null=True)
    pickUpPoint = models.BooleanField(default=False)
    orderDetails = models.ManyToManyField(OrderDetails, blank=True, null=True)
    transportDetails = models.ForeignKey(TransportDetails, on_delete=models.CASCADE, null=True, blank=True)
    customerDetails = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True, blank=True)
    billingDetails = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return self.shipmentId or ''
