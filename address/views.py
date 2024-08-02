from .serializers import AddressSerializer, AddressforleaseSerializer
from .models import address
from rest_framework.views import APIView
from rest_framework.response import Response


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework import status
from owner.models import User

@method_decorator(csrf_exempt, name='dispatch')

class AddressView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Area=request.data.get('Area')
        Building_name=request.data.get('Building_name')
        Floor=request.data.get('Floor')
        Flat_no=request.data.get('Flat_no')
        present=address.objects.filter(Area=Area,Building_name=Building_name,Floor=Floor,Flat_no=Flat_no)
        print(present)
        if present:
            return Response({'detail': 'Address already Present'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



@method_decorator(csrf_exempt, name='dispatch')
class GetAddress(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.user
        data=User.objects.filter(email=email).values("id")
        owner_id=data[0]["id"]
        address_data=address.objects.filter(owner_id=owner_id)
        if address_data:
            addr_seril = AddressSerializer(address_data, many=True)
            return Response(addr_seril.data)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class GetsingleAddress(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        id=request.GET.get('address_id')
        address_data=address.objects.filter(id=id)
        if address_data:
            addr_seril = AddressSerializer(address_data, many=True)
            return Response(addr_seril.data)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)






@method_decorator(csrf_exempt, name='dispatch')
class Addressforleaseview(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.user
        data=User.objects.filter(email=email).values("id")
        owner_id=data[0]["id"]
        address_data=address.objects.filter(owner_id=owner_id, is_on_rent=0)
        if address_data:
            addr_seril = AddressforleaseSerializer(address_data, many=True)
            return Response(addr_seril.data)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)
