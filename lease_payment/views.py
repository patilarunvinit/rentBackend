from .serializers import leaseSerializer
from .models import lease

from address.models import address
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
        address_id = request.data.get('address_id')
        print(address_id)
        address1 = address.objects.filter(id=address_id).first()
        if address_id:
            address1.is_on_rent = 1
            address1.save()
        serializer = leaseSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)




