from django.db import models


# Create your models here.
class address(models.Model):
    owner_id=models.IntegerField(null=True)
    Area = models.CharField(max_length=500)
    Building_name = models.CharField(max_length=500)
    Floor = models.CharField(max_length=25)
    Flat_no = models.CharField(max_length=25)
    Rent = models.IntegerField()
    is_on_rent= models.BooleanField(default=False, null=True)

