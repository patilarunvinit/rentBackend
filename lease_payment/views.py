from .serializers import leaseSerializer
from .models import lease,Payment

from address.models import address
from rest_framework.views import APIView
from rest_framework.response import Response


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework import status
from owner.models import User
from address.models import address
from renter.models import renter

from datetime import date
from dateutil.relativedelta import relativedelta



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
            serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)




@method_decorator(csrf_exempt, name='dispatch')
class getleaseforrent(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        reqdate=request.GET.get('date')
        email = request.user
        data=User.objects.filter(email=email).values("id")
        owner_id=data[0]["id"]
        address_id=address.objects.filter(owner_id=owner_id,is_on_rent=1).values_list('id', flat=True)
        address_ids_list = list(address_id)
        lease_data = lease.objects.filter(address_id__in=address_ids_list)
        # print(lease_data)
        today = date.today()
        print(today)
        main_list=[]
        for leasedata in lease_data:
            end_date = today - relativedelta(months=1)
            lease_list = []
            while leasedata.start_date <= end_date:
                # month_list.append(leasedata.start_date .strftime('%Y-%m'))
                leasedata.start_date  += relativedelta(months=1)
                dateformonth=(leasedata.start_date- relativedelta(months=1)) .strftime('%Y-%m')
                lease_id=leasedata.id
                rent=leasedata.rent
                renter_name=renter.objects.filter(id=leasedata.renter_id).values('renter_name')
                addressdata=address.objects.filter(id=leasedata.address_id).values('Area','Building_name','Floor','Flat_no')
                paid=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth).values('paid')
                date_of_pay=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth).values('date_of_pay')
                # print(lease_id,dateformonth,rent,renter_name[0]["renter_name"],addressdata[0]["Area"],addressdata)
                if reqdate == dateformonth:
                    lease_list.append({"lease_id": lease_id})
                    lease_list.append({"dateformonth": dateformonth})
                    lease_list.append({"rent": rent})
                    lease_list.append({"renter_name": renter_name[0]["renter_name"]})
                    lease_list.append({"addressdata": addressdata[0]["Area"]})
                    lease_list.append({"paid": paid})
                    lease_list.append({"date_of_pay": date_of_pay})
                    main_list.append(lease_list)
                else:
                    pass

                # print(lease_list)

                lease_list=[]
        # print(main_list)
        if main_list:
            return Response(main_list)

        return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class getmonths(APIView):
        authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            email = request.user
            data = User.objects.filter(email=email).values("id")
            owner_id = data[0]["id"]
            address_id = address.objects.filter(owner_id=owner_id, is_on_rent=1).values_list('id', flat=True)
            address_ids_list = list(address_id)
            lease_data = lease.objects.filter(address_id__in=address_ids_list)
            today = date.today()
            main_list = []
            for leasedata in lease_data:
                end_date = today - relativedelta(months=1)
                while leasedata.start_date <= end_date:
                    leasedata.start_date += relativedelta(months=1)
                    dateformonth = (leasedata.start_date - relativedelta(months=1)).strftime('%Y-%m')
                    date_dict = {"dateformonth": dateformonth}
                    if date_dict in main_list:
                        pass
                    else:
                        main_list.append(date_dict)



            if main_list:
                return Response(main_list)

            return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)

    #
    # def get(self, request):
    #
    #     dateformonth=request.GET.get('dateformonth')
    #     print(dateformonth)
    #     email = request.user
    #     data=User.objects.filter(email=email).values("id")
    #     owner_id=data[0]["id"]
    #     address_id=address.objects.filter(owner_id=owner_id,is_on_rent=1).values_list('id', flat=True)
    #     address_ids_list = list(address_id)
    #     lease_data = lease.objects.filter(address_id__in=address_ids_list)
    #     # print(lease_data)
    #     today = date.today()
    #     print(today)
    #     main_list=[]
    #     for leasedata in lease_data:
    #         end_date = today - relativedelta(months=1)
    #         lease_list = []
    #         while leasedata.start_date <= end_date:
    #             # month_list.append(leasedata.start_date .strftime('%Y-%m'))
    #             leasedata.start_date  += relativedelta(months=1)
    #             dateformonth=(leasedata.start_date- relativedelta(months=1)) .strftime('%Y-%m')
    #             lease_id=leasedata.id
    #             rent=leasedata.rent
    #             renter_name=renter.objects.filter(id=leasedata.renter_id).values('renter_name')
    #             addressdata=address.objects.filter(id=leasedata.address_id).values('Area','Building_name','Floor','Flat_no')
    #             paid=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth).values('paid')
    #             date_of_pay=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth).values('date_of_pay')
    #             # print(lease_id,dateformonth,rent,renter_name[0]["renter_name"],addressdata[0]["Area"],addressdata)
    #             lease_list.append({"lease_id":lease_id})
    #             lease_list.append({"dateformonth":dateformonth})
    #             lease_list.append({"rent":rent})
    #             lease_list.append({"renter_name":renter_name[0]["renter_name"]})
    #             lease_list.append({"addressdata":addressdata[0]["Area"]})
    #             lease_list.append({"paid":paid})
    #             lease_list.append({"date_of_pay":date_of_pay})
    #             # print(lease_list)
    #             main_list.append(lease_list)
    #             lease_list=[]
    #     print(main_list)
    #     if main_list:
    #         return Response(main_list)
    #
    #     return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)
