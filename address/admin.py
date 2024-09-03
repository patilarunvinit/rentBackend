from django.contrib import admin
from .models import address
from import_export.admin import ImportExportModelAdmin



class AddressAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display =('id','owner_id', 'Area', 'Building_name', 'Floor','Flat_no', 'Rent','is_on_rent')


admin.site.register(address, AddressAdmin)