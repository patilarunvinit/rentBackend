from django.db import models


# Create your models here.
class lease(models.Model):
    owner_id=models.IntegerField()
    renter=models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)



class Payment(models.Model):
    lease_id = models.IntegerField()
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    remain = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_pay = models.DateField()
    for_month = models.CharField(max_length=7)  # Format: YYYY-MM
    transaction_mode = models.CharField(max_length=50)