from rest_framework import serializers
from .models import User,OTP
from django.contrib.auth.hashers import make_password


# Main Serializer of user(owner)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'mobile_no', 'b_date', 'owner_photo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        print(user.password)
        if password:
            user.set_password(password)
        user.save()
        return user



# Serializer of OTP request
class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Serializer of OTP Verification
class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

# Serializer of OTP Password Reset
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8)