from django.db import models

# Create your models here.
class SellerProfile(models.Model):
    seller_name = models.CharField(max_length=255, blank=False, null=False)
    client_id = models.CharField(max_length=255, blank=False, null=False)
    client_secret = models.CharField(max_length=255, blank=False, null=False)
    access_token = models.TextField(blank=False)

    def __str__(self):
        return self.seller_name

    class Meta:
        unique_together = (('seller_name', 'client_id', 'client_secret'), )


# class AccessToken(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     access_token = models.TextField(blank=False)
#
#     def __str__(self):
#         return self.user.username