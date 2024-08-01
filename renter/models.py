from django.db import models


# Create your models here.
class renter(models.Model):
    owner_id=models.IntegerField()
    renter_name = models.CharField(max_length=60)
    renter_mobile_no = models.IntegerField()
    id_type = models.CharField(max_length=30)
    id_img = models.ImageField(upload_to='images/', null=True, verbose_name="")

