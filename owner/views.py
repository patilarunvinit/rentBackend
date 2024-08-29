from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import UserSerializer ,OTPRequestSerializer, OTPVerificationSerializer,PasswordResetSerializer
from .models import User , OTP
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

import random
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.utils import timezone

class RegisterView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# For Test
@csrf_exempt
def testget(request):
    if request.method == "GET":
        sdata = User.objects.all()
        s1data = UserSerializer(sdata, many=True)
        return JsonResponse(s1data.data, safe=False)

#For Owner Login
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Invalid Email')
        elif user and not user.check_password(password):
            raise AuthenticationFailed('Invalid Password')
        elif user is None or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Set JWT as cookie and return in response
        response = Response()
        response.set_cookie(key='jwt', value=access_token, httponly=True, secure=True, samesite='Lax')
        response.data = {
            'access': access_token,
            'refresh': str(refresh),
        }

        return response


@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        email = request.user
        try:
            maindata = User.objects.filter(email=email).first()
            serializer = UserSerializer(maindata)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(email=email).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class AccessRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = token.access_token
            # if token.blacklisted:
            #     return Response({'detail': 'Invalid or blacklisted refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'access': str(new_access_token)}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)













@method_decorator(csrf_exempt, name='dispatch')
class OTPRequestView(APIView):
    def post(self, request):
        print(request.data)
        serializer = OTPRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            otp_code = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
            expires_at = timezone.now() + timedelta(minutes=10)  # OTP valid for 10 minutes

            # Delete any existing OTPs for the user
            OTP.objects.filter(user=user).delete()

            user_name = user.name
            OTP.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)
            message = (
                f"Dear {user_name},\n\n"
                f"Thank you for using RentPro. We have received a request to verify your identity.\n\n"
                f"Your OTP code is:\n"
                f"{otp_code}\n\n"
                f"This code is valid for the next 10 minutes. Please enter this code in the application to complete your verification process.\n\n"
                f"If you did not request this code, please ignore this email or contact our support team for assistance.\n\n"
                f"Best regards,\n\n"
                f"Mrent\n"
                f"kasheli (koliwada)\n"
                f"Thane, 421302\n"
                f"adnyatech@gmail.com\n"
                f"(91) 7900079060\n"
            )
            send_mail(
                'Your OTP Code for Password Change',
                 message,
                'no-reply@example.com',  # Replace with your FROM email address
                [email],
            )
            return Response({'message': 'OTP sent to email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)





@method_decorator(csrf_exempt, name='dispatch')
class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        print(serializer)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user, otp_code=otp_code).first()
            if otp and otp.is_valid():
                return Response({'message': 'OTP verified.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)





@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        # print(serializer)
        if not serializer.is_valid():
            print("work")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        try:
            user = User.objects.get(email=email)
            print(user)
            user.set_password(new_password)
            user.save()
            # Optionally, delete all OTPs for this user
            OTP.objects.filter(user=user).delete()
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            # Extract the refresh token from the request
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            r_token = RefreshToken(refresh_token)
            r_token.blacklist()  # Blacklist the refresh token
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({'detail': 'Token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

#test done
























