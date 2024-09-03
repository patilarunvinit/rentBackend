from django.contrib import admin
from .models import lease,Payment
from import_export.admin import ImportExportModelAdmin



class leaseAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display =('id', 'address_id', 'renter_id', 'start_date', 'end_date', 'rent', 'deposit')


admin.site.register(lease, leaseAdmin)


class paymentAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display =('id', 'lease_id', 'paid', 'remain', 'date_of_pay', 'for_month', 'transaction_mode','is_remain_pay')


admin.site.register(Payment, paymentAdmin)