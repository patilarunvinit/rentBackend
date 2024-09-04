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
from address.models import address




# To store renter with owner_id(user)
@method_decorator(csrf_exempt, name='dispatch')
class renterView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        renter_name=request.data.get('renter_name')
        owner_id=request.data.get('owner_id')
        present=renter.objects.filter(renter_name=renter_name)
        if present:
            return Response({'detail': 'Renter already Present'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = renterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            last_error_message = get_last_error_message(serializer.errors)
            return Response({'detail': last_error_message}, status=status.HTTP_400_BAD_REQUEST)


# to get error msg fun
def get_last_error_message(errors):
    all_errors = [msg for field_errors in errors.values() for msg in field_errors]
    return all_errors[-1] if all_errors else ""



# renter list for add lease
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

        return Response({'detail': 'You Need Add Renter First'}, status=status.HTTP_400_BAD_REQUEST)






# To Get Renter on Lease
@method_decorator(csrf_exempt, name='dispatch')
class Getrenterifonlease(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        address_id=request.GET.get('address_id')
        renter_id=lease.objects.filter(address_id=address_id).values_list('renter_id', flat=True).first()

        if renter_id:
            # get address on lease
            address1 = address.objects.filter(id=address_id,is_on_rent=0)
            start_date = lease.objects.filter(address_id=address_id).values("start_date")
            if address1:
                return Response({'detail': 'Renter Dont Have Lease'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                extra_data = {
                    'start_date': start_date[0]['start_date'],
                }
                renter_data = renter.objects.filter(id=renter_id).first()
                addr_seril = renterSerializer(renter_data, many=False)
                return Response([addr_seril.data, extra_data])

        return Response({'detail': 'Address Is Not On Lease'}, status=status.HTTP_400_BAD_REQUEST)


#test