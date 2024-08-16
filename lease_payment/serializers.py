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
        fields = ['id', 'lease_id', 'paid', 'remain', 'date_of_pay', 'for_month', 'transaction_mode','is_remain_pay']

    def create(self, validated_data):
            instance = self.Meta.model(**validated_data)
            instance.save()
            return instance


class remainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'lease_id', 'paid', 'remain', 'date_of_pay', 'for_month', 'transaction_mode', 'is_remain_pay']

    def validate(self, data):
        # Ensure 'remain' is always set to 0
        data['remain'] = 0
        return data

    def create(self, validated_data):
        # 'remain' is already set to 0 by the validate method
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance



