from django.db import models



class lease(models.Model):
    address_id=models.IntegerField()
    renter_id=models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)



class Payment(models.Model):
    lease_id = models.IntegerField()
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    remain = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_pay = models.DateField(null=True)
    for_month = models.CharField(max_length=7, blank=True, null=True)  # Format: YYYY-MM
    transaction_mode = models.CharField(max_length=50,null=True, blank=True)
    is_remain_pay = models.BooleanField(null=True, default=0)

