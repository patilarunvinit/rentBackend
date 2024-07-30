from .serializers import AddressSerializer

from rest_framework.views import APIView
from rest_framework.response import Response


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

@method_decorator(csrf_exempt, name='dispatch')

class AddressView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)