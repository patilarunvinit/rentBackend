from rest_framework import serializers
from .models import lease, Payment
from django import forms
from django.contrib.auth.hashers import make_password

class leaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = lease
        fields = ['id', 'address_id', 'renter_id', 'start_date', 'end_date', 'rent', 'deposit']

    def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance

class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'lease_id', 'paid', 'remain', 'date_of_pay', 'for_month', 'transaction_mode']

    def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance


