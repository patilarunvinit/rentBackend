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
from lease_payment.models import lease

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
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data)
        else:
            consolidated_message = all_fields_required(serializer.errors)
            if consolidated_message:
                return Response({'detail': consolidated_message}, status=status.HTTP_400_BAD_REQUEST)

            last_error_message = get_last_error_message(serializer.errors)
            return Response({'detail': last_error_message}, status=status.HTTP_400_BAD_REQUEST)

        # return Response(serializer.data)

def get_last_error_message(errors):
   all_errors = [msg for field_errors in errors.values() for msg in field_errors]
   return all_errors[-1] if all_errors else ""

def all_fields_required(errors):
    # Check if all errors are "This field is required."
    required_errors = all(
        all(error.code == 'required' for error in field_errors)
        for field_errors in errors.values()
    )
    if required_errors:
        return "All fields are required."
    return None



@method_decorator(csrf_exempt, name='dispatch')
class GetAddress(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.user
        data=User.objects.filter(email=email).values("id")
        owner_id=data[0]["id"]
        available = request.GET.get('available')
        print(available)
        if available == "all":
            address_data=address.objects.filter(owner_id=owner_id)
        elif available == "1":
            print("yes")
            address_data=address.objects.filter(owner_id=owner_id,is_on_rent=available)
        elif available == "0":
            address_data=address.objects.filter(owner_id=owner_id,is_on_rent=available)

        if address_data:
            addr_seril = AddressSerializer(address_data, many=True)
            return Response(addr_seril.data)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class GetsingleAddress(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        id = request.GET.get('address_id')
        address_data = address.objects.filter(id=id)
        email = request.user
        name = User.objects.filter(email=email).values("name")
        extra_data = {
                'owner_name': name[0]['name'],
            }



        if address_data:
            addr_seril = AddressSerializer(address_data, many=True)
            return Response([addr_seril.data,extra_data])

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





@method_decorator(csrf_exempt, name='dispatch')
class Addresscountview(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.user
        data=User.objects.filter(email=email).values("id")
        owner_id=data[0]["id"]
        address_data=address.objects.filter(owner_id=owner_id)
        address_count=len(address_data)
        if address_count:
            responce={
                "addresscount":address_count
            }
            return Response(responce)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)









@method_decorator(csrf_exempt, name='dispatch')
class Addressonleaseview(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.user
        data=User.objects.filter(email=email).values("id")
        owner_id=data[0]["id"]
        address_data=address.objects.filter(owner_id=owner_id, is_on_rent=1)
        if address_data:
            addr_seril = AddressforleaseSerializer(address_data, many=True)
            return Response(addr_seril.data)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)
