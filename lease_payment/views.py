from .serializers import leaseSerializer
from .models import lease
from rest_framework.views import APIView
from rest_framework.response import Response


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework import status
from owner.models import User

@method_decorator(csrf_exempt, name='dispatch')
class leaseView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        renter_name=request.data.get('renter_name')
        present=lease.objects.filter(renter_name=renter_name)
        print(present)
        if present:
            return Response({'detail': 'lease already Present'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = leaseSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
