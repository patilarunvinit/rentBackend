from rest_framework import serializers
from .models import renter
from django import forms
from django.contrib.auth.hashers import make_password

class renterSerializer(serializers.ModelSerializer):
    class Meta:
        model = renter
        fields = ['id','owner_id', 'renter_name', 'renter_mobile_no', 'id_type', 'id_img']



    def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance