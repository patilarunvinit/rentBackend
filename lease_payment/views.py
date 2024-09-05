from django.db.models import Sum
from .serializers import leaseSerializer, paymentSerializer ,remainSerializer
from .models import lease,Payment
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
from django.utils.dateparse import parse_date





# To make payment of month
@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(APIView):
    # Use JWTAuthentication
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = paymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)







# To make remain payment of month
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
            # subtract remain from main payment and make change in that payment
            Payment.objects.filter(lease_id=lease_id_value,for_month=for_month_value, is_remain_pay=0).update(remain=remain_value)
            # store remain paymeny on database
            serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)




# To make full remain payment of all remain months
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
            # because of user paid full rent of lease all main payment remains will be 0 now
            Payment.objects.filter(lease_id=lease_id, for_month__in=months_list, is_remain_pay=0) .update(remain=0)
            # subtract remain from main payment and make change in that payment
            serializer.save()
            return Response(serializer.data)
        else:
            pass
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)









# To add lease
@method_decorator(csrf_exempt, name='dispatch')
class leaseView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        address_id = request.data.get('address_id')
        address1 = address.objects.filter(id=address_id).first()
        if address_id:
            # make address not available
            address1.is_on_rent = 1
            address1.save()
        serializer = leaseSerializer(data=request.data)
        if serializer.is_valid():
            # store new lease in database
            serializer.save()
            return Response(serializer.data)
        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)







# To remove lease (add last date and make address available)
@method_decorator(csrf_exempt, name='dispatch')
class removeleaseView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        address_id = request.data.get('address_id')
        end_date = request.data.get('end_date')

        if address_id:
            # add last date in lease (end lease for address)
            lease.objects.filter(address_id=address_id).update(end_date=end_date)
            # make change in address availability (kame it available)
            address.objects.filter(id=address_id).update(is_on_rent=0)
            return Response({'detail': 'Lease Removed'})

        return Response({'detail': 'Some Think Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)







# make lease for selected month
@method_decorator(csrf_exempt, name='dispatch')
class getleaseforrent(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # get month for lease
        reqdate=request.GET.get('date')
        email = request.user
        # get user data for login user
        data=User.objects.filter(email=email).values("id")
        # get owner id from user(owner) data
        owner_id=data[0]["id"]
        # from user(owner) id we get all address id's
        address_id=address.objects.filter(owner_id=owner_id,is_on_rent=1).values_list('id', flat=True)
        # convert address id's into list
        address_ids_list = list(address_id)
        # get a list of lease info from address id's
        lease_data = lease.objects.filter(address_id__in=address_ids_list,end_date__isnull=True)
        # get today's date
        today = date.today()
        # mark end date to get last lease (last month lease)
        end_date = today - relativedelta(months=1)
        # change date formate into month-year
        end_date_month = end_date.strftime('%Y-%m')
        main_list=[]
        # to get list of lease for each month
        for leasedata in lease_data:
            lease_list = []
            lease_id = leasedata.id
            rent_of_lease = lease.objects.filter(id=lease_id).values('rent')
            # loop for lease from start date to end date
            while leasedata.start_date <= end_date:
                # get start date from lease table and add 1 month to start lease
                leasedata.start_date  += relativedelta(months=1)
                # make date formate to month-year formate
                dateformonth=(leasedata.start_date - relativedelta(months=1)) .strftime('%Y-%m')
                if dateformonth==end_date_month:
                    pass
                else:
                    # check where lease already paid
                    paid = Payment.objects.filter(lease_id=lease_id, for_month=dateformonth,is_remain_pay=0).values('paid')
                    if paid:
                        pass
                    else:
                        # if not and lease is not for last month then add 0 payment fpr that month
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
                        if serializer.is_valid():
                            serializer.save()

                # now get data to pass to front end of selected date
                rent=leasedata.rent
                renter_name=renter.objects.filter(id=leasedata.renter_id).values('renter_name')
                addressdata=address.objects.filter(id=leasedata.address_id).values('Area','Building_name','Floor','Flat_no')
                paid=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth,is_remain_pay=0).values('paid')
                date_of_pay=Payment.objects.filter(lease_id=lease_id,for_month=dateformonth).values('date_of_pay')
                # compare selected date and loop months
                if reqdate == dateformonth:
                    lease_list.append({"lease_id": lease_id})
                    lease_list.append({"dateformonth": dateformonth})
                    lease_list.append({"rent": rent})
                    lease_list.append({"renter_name": renter_name[0]["renter_name"]})
                    lease_list.append({"addressdata": addressdata})
                    lease_list.append({"paid": paid})
                    lease_list.append({"date_of_pay": date_of_pay})
                    main_list.append(lease_list)
                # pass all other months that not selected
                else:
                    pass

                # make list empty to store other lease payment
                lease_list=[]
        # if there is any lease for selected date send a lease
        if main_list:
            return Response(main_list)
        if lease_data:
            return Response({'detail': 'No leases available this month'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'No Address Is On Lease'}, status=status.HTTP_400_BAD_REQUEST)








# To get month list for user if lease present
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
            # get lease from user(owner) address id's list
            lease_data = lease.objects.filter(address_id__in=address_ids_list,end_date__isnull=True)
            # today dates
            today = date.today()
            main_list = []
            for leasedata in lease_data:
                # make last date by subtracting 1 month
                end_date = today - relativedelta(months=1)
                to_last_date = {"dateformonth": end_date.strftime('%Y-%m')}
                # loop from start date to last date
                while leasedata.start_date <= end_date:
                    leasedata.start_date += relativedelta(months=1)
                    dateformonth = (leasedata.start_date - relativedelta(months=1)).strftime('%Y-%m')
                    # get date (month-year)
                    date_dict = {"dateformonth": dateformonth}
                    # if date id already in list then pass else store in list
                    if date_dict in main_list:
                        pass
                    else:
                        main_list.append(date_dict)


            if to_last_date not in main_list:
                main_list.append(to_last_date)
            # descending order a list of month
            main_list.sort(key=lambda x: parse_date(x["dateformonth"] + '-01'), reverse=True)


            if main_list:
                return Response(main_list)

            return Response({'detail': 'No Address Is On Lease'}, status=status.HTTP_400_BAD_REQUEST)









# To get remain of all renter of owner (if remain)
@method_decorator(csrf_exempt, name='dispatch')
class getremiain(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.user
        data = User.objects.filter(email=email).values("id")
        owner_id = data[0]["id"]
        address_id = address.objects.filter(owner_id=owner_id, is_on_rent=1).values_list('id', flat=True)
        address_ids_list = list(address_id)
        lease_ids = lease.objects.filter(address_id__in=address_ids_list,end_date__isnull=True).values_list('id', flat=True)
        # get list of lease id's for owner address
        lease_ids_list = list(lease_ids)
        # get lease sum of remain
        payment_data = Payment.objects.filter(lease_id__in=lease_ids_list).values('lease_id').annotate(
            total_remain=Sum('remain')).values('lease_id', 'total_remain')
        remain_list = []
        main_remain = []
        # loop for every renter
        for pay in payment_data:
            # check if total remain of renter if 0 or not
            if pay['total_remain'] <= 0:
                continue

            # if not 0 then collect data to send
            deposit = lease.objects.filter(id=pay['lease_id']).values('deposit')
            renter_id = lease.objects.filter(id=pay['lease_id']).values('renter_id')
            renter_name = renter.objects.filter(id=renter_id[0]["renter_id"]).values('renter_name')
            remain_list.append({"lease_id": pay['lease_id']})
            remain_list.append({"remain": pay['total_remain']})
            remain_list.append({"deposit": deposit[0]["deposit"]})
            remain_list.append({"renter_name": renter_name[0]["renter_name"]})
            main_remain.append(remain_list)
            # empty a list to add next remain
            remain_list = []

        if main_remain:
            return Response(main_remain)

        return Response({'detail': 'No Remain To Pay'}, status=status.HTTP_400_BAD_REQUEST)








# get remain history (every month remain history) of selected renter
@method_decorator(csrf_exempt, name='dispatch')
class getremianhistory(APIView):
        authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            # collecting a data of renter to send
            lease_id = request.GET.get('lease_id')
            lease_data = lease.objects.filter(id=lease_id).values('address_id','renter_id')
            address_data=address.objects.filter(id=lease_data[0]["address_id"]).values('Area','Building_name','Floor','Flat_no').first()
            renter_name = renter.objects.filter(id=lease_data[0]["renter_id"]).values('renter_name').first()
            deposit = lease.objects.filter(id=lease_id).values('deposit')
            pay_data = Payment.objects.filter(lease_id=lease_id,remain__gt=0).values("lease_id","remain","paid","for_month")
            total_remain = Payment.objects.filter(lease_id=lease_id).values('lease_id').annotate(total_remain=Sum('remain')).values( 'total_remain')



            rent_info=[address_data,renter_name,deposit,total_remain]

            if pay_data:
                return Response({'rent_info': rent_info,'remain_data':pay_data})
            return Response({'detail': 'No Remain Data'}, status=status.HTTP_400_BAD_REQUEST)









# get info of selected address remain data(renter_name,full_remain,deposit) to make last remove lease
@method_decorator(csrf_exempt, name='dispatch')
class getremovedata(APIView):
        authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            # collecting a data to send
            address_id = request.GET.get('address_id')
            deposit = lease.objects.filter(address_id=address_id).values('deposit')
            lease_id = lease.objects.filter(address_id=address_id).values('id')
            total_remain = Payment.objects.filter(lease_id=lease_id[0]['id']).values('lease_id').annotate(total_remain=Sum('remain')).values( 'total_remain')
            deposite_to_pay = deposit[0]['deposit'] - total_remain[0]['total_remain']
            renter_id = lease.objects.filter(id=lease_id[0]['id']).values('renter_id').first()
            renter_name = renter.objects.filter(id=renter_id['renter_id']).values('renter_name').first()

            # data formate to send
            response_data = {
                'renter_name': renter_name['renter_name'],
                'total_remain': float(total_remain[0]['total_remain']),
                'deposite_to_pay': float(deposite_to_pay),
                'deposit': float(deposit[0]['deposit']),
            }


            if response_data:
                return Response(response_data)
            return Response({'detail': 'No Data To Remove'}, status=status.HTTP_400_BAD_REQUEST)

