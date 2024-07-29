from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import UserSerializer
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions





class RegisterView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@csrf_exempt
def testget(request):
    if request.method == "GET":
        sdata = User.objects.all()
        s1data = UserSerializer(sdata, many=True)
        return JsonResponse(s1data.data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials.')

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

        user = User.objects.filter(id=11).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            # Extract the refresh token from the request
            refresh_token = request.data.get('refresh')
            print(refresh_token)
            if not refresh_token:
                return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({'detail': 'Token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

#test done