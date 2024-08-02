from .serializers import renterSerializer, RenterforleaseSerializer
from .models import renter
from rest_framework.views import APIView
from rest_framework.response import Response


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework import status
from owner.models import User
from lease_payment.models import lease

@method_decorator(csrf_exempt, name='dispatch')
class renterView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        renter_name=request.data.get('renter_name')
        # print('Request Data:', request.data)
        # print('Request Files:', request.FILES.get('id_img'))
        present=renter.objects.filter(renter_name=renter_name)
        print(present)
        if present:
            return Response({'detail': 'Renter already Present'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = renterSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




# class GetAddress(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request):
#         email = request.user
#         data=User.objects.filter(email=email).values("id")
#         owner_id=data[0]["id"]
#         address_data=address.objects.filter(owner_id=owner_id)
#         if address_data:
#             addr_seril = AddressSerializer(address_data, many=True)
#             return Response(addr_seril.data)
#
#         return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class renterforleaseview(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.user
        data=User.objects.filter(email=email).values("id")
        owner_id=data[0]["id"]
        renter_data=renter.objects.filter(owner_id=owner_id)
        if renter_data:
            addr_seril = RenterforleaseSerializer(renter_data, many=True)
            return Response(addr_seril.data)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class Getrenterifonlease(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        address_id=request.GET.get('address_id')
        renter_id=lease.objects.filter(address_id=address_id).values_list('renter_id', flat=True).first()
        print(renter_id)
        if renter_id:
            renter_data= renter.objects.filter(id=renter_id).first()
            addr_seril = renterSerializer(renter_data, many=False)
            return Response(addr_seril.data)

        return Response({'detail': 'Address Is Not On Lease'}, status=status.HTTP_400_BAD_REQUEST)
