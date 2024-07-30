from rest_framework import serializers
from .models import address
from django.contrib.auth.hashers import make_password

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = address
        fields = ['id','owner_id', 'Area', 'Building_name', 'Floor','Flat_no', 'Rent','is_on_rent']


    def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance