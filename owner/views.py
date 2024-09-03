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




# To register user (owner)
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






# For uswer(Owner) Login
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        # get email and password from request
        email = request.data.get('email')
        password = request.data.get('password')

        # check is input are empty or not
        if not email or not password:
            return Response({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        # check validations
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



# To get user(owner) data
@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    # check user is authenticated
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        email = request.user

        # check user is present in database
        try:
            maindata = User.objects.filter(email=email).first()
            # seriaizer a filter data
            serializer = UserSerializer(maindata)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise AuthenticationFailed('Unauthenticated!')

        # extra fun for same
        user = User.objects.filter(email=email).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)





# refresh a access token with help of refresh token
@method_decorator(csrf_exempt, name='dispatch')
class AccessRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        # if refresh token is not present
        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            #create new access token
            token = RefreshToken(refresh_token)
            new_access_token = token.access_token

            # check if refresh token is not valid (black listed)
            if token.check_blacklist():
                return Response({'detail': 'Invalid or blacklisted refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'access': str(new_access_token)}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)












# To send OTP in Email
@method_decorator(csrf_exempt, name='dispatch')
class OTPRequestView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)

        # If Email not in database
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            # Generate a 6-digit OTP
            otp_code = str(random.randint(100000, 999999))
            # OTP valid for 10 minutes
            expires_at = timezone.now() + timedelta(minutes=10)

            # Delete any existing OTPs for the user
            OTP.objects.filter(user=user).delete()

            user_name = user.name
            OTP.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)
            message = (
                f"Dear {user_name},\n\n"
                f"Thank you for using Mrent. We have received a request to verify your identity.\n\n"
                f"Your OTP code is:\n"
                f"{otp_code}\n\n"
                f"This code is valid for the next 10 minutes. Please enter this code in the application to complete your verification process.\n\n"
                f"If you did not request this code, please ignore this email or contact our support team for assistance.\n\n"
                f"Best regards,\n\n"
                f"Mrent\n"
                f"kasheli (koliwada)\n"
                f"Thane, 421302\n"
                f"adnyatech@gmail.com\n"
                f"(+91) 7900079060\n"
            )
            send_mail(
                'Your OTP Code for Password Change',
                 message,
                'adnyatech@gmail.com',
                [email],
            )
            return Response({'message': 'OTP sent to email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)






# To verify OTP from user
@method_decorator(csrf_exempt, name='dispatch')
class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        # check OTP in database
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user, otp_code=otp_code).first()
            # validate email and OTP
            if otp and otp.is_valid():
                return Response({'message': 'OTP verified.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)






# To change password
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        # check serializer validation
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        try:
            # save change in password
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # Optionally, delete all OTPs for this user
            OTP.objects.filter(user=user).delete()
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=status.HTTP_400_BAD_REQUEST)






# user(owner) Logout
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
            # Blacklist the refresh token
            r_token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({'detail': 'Token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)


























