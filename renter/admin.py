from django.contrib import admin
from .models import renter
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class renterAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display =('id','owner_id', 'renter_name', 'renter_mobile_no', 'id_type', 'id_img')


admin.site.register(renter, renterAdmin)
