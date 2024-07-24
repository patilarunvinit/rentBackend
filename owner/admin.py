from django.contrib import admin
from .models import User
from .serializers import UserSerializer

class UserAdmin(admin.ModelAdmin):
   list_display = ['email', 'name', 'is_staff']
   search_fields = ['email', 'name']
admin.site.register(User)