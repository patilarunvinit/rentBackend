from django.db.models import Sum

from .serializers import leaseSerializer, paymentSerializer ,remainSerializer
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

#test
from twilio.rest import Client
from django.utils.dateparse import parse_date



@method_decorator(csrf_exempt, name='dispatch')
class testview(APIView):

        def get(self, request):
            ACCOUNT_SID = ''
            AUTH_TOKEN = ''

            # Create a client instance
            client = Client(ACCOUNT_SID, AUTH_TOKEN)

            # Your Twilio WhatsApp sandbox number
            from_whatsapp_number = ''  # Twilio sandbox number

            # Recipient's phone number (must be in the format 'whatsapp:+1234567890')
            to_whatsapp_number = ''

            # Message you want to send
            message_body = 'Hello, this is a test message from Twilio!'

            # Send the message
            message = client.messages.create(
                body=message_body,
                from_=from_whatsapp_number,
                to=to_whatsapp_number
            )
            print(f"Status: {message.status}")

            return Response({'detail': 'msg send'})



@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = paymentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print("work")
            # serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)




@method_decorator(csrf_exempt, name='dispatch')
class RemainPayView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        remain_value = request.data.get('remain', None)
        for_month_value = request.data.get('for_month', None)
        lease_id_value = request.data.get('lease_id', None)

        serializer = remainSerializer(data=request.data)
        if serializer.is_valid():
            # Payment.objects.filter(lease_id=lease_id_value,for_month=for_month_value, is_remain_pay=0).update(remain=remain_value)
            # serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)





@method_decorator(csrf_exempt, name='dispatch')
class fullRemainPayView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        form_data = request.data['fullpaydata']
        lease_id = request.data['fullpaydata']['lease_id']
        months = request.data['for_months']
        months_list = [month.get('for_month') for month in months]

        serializer = remainSerializer(data=form_data)
        if serializer.is_valid():
            # Payment.objects.filter(lease_id=lease_id, for_month__in=months_list, is_remain_pay=0) .update(remain=0)
            # serializer.save()
            return Response(serializer.data)
        else:
            print("Errors:", serializer.errors)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)










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
            # address1.save()
        serializer = leaseSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)








@method_decorator(csrf_exempt, name='dispatch')
class removeleaseView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        address_id = request.data.get('address_id')
        end_date = request.data.get('end_date')

        if address_id:
            # lease.objects.filter(address_id=address_id).update(end_date=end_date)
            # address.objects.filter(id=address_id).update(is_on_rent=0)
            return Response({'detail': 'Lease Removed'})

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
        # print(today)
        end_date = today - relativedelta(months=1)
        end_date_month = end_date.strftime('%Y-%m')
        main_list=[]
        for leasedata in lease_data:
            lease_list = []
            lease_id = leasedata.id
            rent_of_lease = lease.objects.filter(id=lease_id).values('rent')
            while leasedata.start_date <= end_date:
                # month_list.append(leasedata.start_date .strftime('%Y-%m'))
                leasedata.start_date  += relativedelta(months=1)
                dateformonth=(leasedata.start_date- relativedelta(months=1)) .strftime('%Y-%m')
                if dateformonth==end_date_month:
                    pass
                else:
                    paid = Payment.objects.filter(lease_id=lease_id, for_month=dateformonth,is_remain_pay=0).values('paid')
                    if paid:
                        pass
                    else:
                        to_save_data={
                            "lease_id": lease_id,
                            "paid": "0.00",
                            "remain": rent_of_lease[0]["rent"],
                            "date_of_pay": None,
                            "for_month": dateformonth,
                            "transaction_mode": "",
                            "is_remain_pay":0,
                        }
                        serializer = paymentSerializer(data=to_save_data)
                        # print(serializer)
                        if serializer.is_valid():
                            serializer.save()

                rent=leasedata.rent
                renter_name=renter.objects.filter(id=leasedata.renter_id).values('renter_name')
                addressdata=address.objects.filter(id=leasedata.address_id).values('Area','Building_name','Floor','Flat_no')
                paid=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth,is_remain_pay=0).values('paid')
                date_of_pay=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth).values('date_of_pay')
                # print(lease_id,dateformonth,rent,renter_name[0]["renter_name"],addressdata[0]["Area"],addressdata)
                if reqdate == dateformonth:
                    lease_list.append({"lease_id": lease_id})
                    lease_list.append({"dateformonth": dateformonth})
                    lease_list.append({"rent": rent})
                    lease_list.append({"renter_name": renter_name[0]["renter_name"]})
                    lease_list.append({"addressdata": addressdata})
                    lease_list.append({"paid": paid})
                    lease_list.append({"date_of_pay": date_of_pay})
                    main_list.append(lease_list)
                else:
                    pass


                lease_list=[]
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

            main_list.sort(key=lambda x: parse_date(x["dateformonth"] + '-01'), reverse=True)

            if main_list:
                return Response(main_list)

            return Response({'detail': 'You Need Add Adrress First'}, status=status.HTTP_400_BAD_REQUEST)








@method_decorator(csrf_exempt, name='dispatch')
class getremiain(APIView):
        authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            email = request.user
            data = User.objects.filter(email=email).values("id")
            owner_id = data[0]["id"]
            address_id = address.objects.filter(owner_id=owner_id, is_on_rent=1).values_list('id', flat=True)
            address_ids_list = list(address_id)
            lease_ids = lease.objects.filter(address_id__in=address_ids_list).values_list('id', flat=True)
            lease_ids_list=list(lease_ids)
            payment_data = Payment.objects.filter(lease_id__in=lease_ids_list).values('lease_id').annotate(total_remain=Sum('remain')).values('lease_id', 'total_remain')
            # print(payment_data)
            remain_list=[]
            main_remain=[]
            for pay in payment_data:
                if pay['total_remain'] <= 0:
                    continue

                deposit = lease.objects.filter(id=pay['lease_id']).values('deposit')
                renter_id = lease.objects.filter(id=pay['lease_id']).values('renter_id')
                renter_name = renter.objects.filter(id=renter_id[0]["renter_id"]).values('renter_name')
                remain_list.append({"lease_id": pay['lease_id']})
                remain_list.append({"remain": pay['total_remain']})
                remain_list.append({"deposit":deposit[0]["deposit"]})
                remain_list.append({"renter_name":renter_name[0]["renter_name"]})
                main_remain.append(remain_list)
                remain_list=[]


            if main_remain:
                return Response(main_remain)

            return Response({'detail': 'No Remain To Pay'}, status=status.HTTP_400_BAD_REQUEST)







@method_decorator(csrf_exempt, name='dispatch')
class getremianhistory(APIView):
        authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            lease_id = request.GET.get('lease_id')
            lease_data = lease.objects.filter(id=lease_id).values('address_id','renter_id')
            address_data=address.objects.filter(id=lease_data[0]["address_id"]).values('Area','Building_name','Floor','Flat_no').first()
            renter_name = renter.objects.filter(id=lease_data[0]["renter_id"]).values('renter_name').first()
            deposit = lease.objects.filter(id=lease_id).values('deposit')
            pay_data = Payment.objects.filter(lease_id=lease_id,remain__gt=0).values("lease_id","remain","paid","for_month")
            total_remain = Payment.objects.filter(lease_id=lease_id).values('lease_id').annotate(total_remain=Sum('remain')).values( 'total_remain')

            print(total_remain)


            rent_info=[address_data,renter_name,deposit,total_remain]

            if pay_data:
                return Response({'rent_info': rent_info,'remain_data':pay_data})
            return Response({'detail': 'No Remain Data'}, status=status.HTTP_400_BAD_REQUEST)










@method_decorator(csrf_exempt, name='dispatch')
class getremovedata(APIView):
        authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            address_id = request.GET.get('address_id')
            deposit = lease.objects.filter(address_id=address_id).values('deposit')
            lease_id = lease.objects.filter(address_id=address_id).values('id')
            total_remain = Payment.objects.filter(lease_id=lease_id[0]['id']).values('lease_id').annotate(total_remain=Sum('remain')).values( 'total_remain')
            deposite_to_pay = deposit[0]['deposit'] - total_remain[0]['total_remain']
            renter_id = lease.objects.filter(id=lease_id[0]['id']).values('renter_id').first()
            renter_name = renter.objects.filter(id=renter_id['renter_id']).values('renter_name').first()

            response_data = {
                'renter_name': renter_name['renter_name'],
                'total_remain': float(total_remain[0]['total_remain']),
                'deposite_to_pay': float(deposite_to_pay),
                'deposit': float(deposit[0]['deposit']),
            }


            if response_data:
                return Response(response_data)
            return Response({'detail': 'No Data To Remove'}, status=status.HTTP_400_BAD_REQUEST)














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
