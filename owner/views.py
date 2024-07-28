from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator





class RegisterView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@csrf_exempt
def testget(request):
    if request.method == "GET":
        sdata = User.objects.all()
        s1data = UserSerializer(sdata, many=True)
        return JsonResponse(s1data.data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        print(request.data)
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            print("no")
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            print("yes")
            raise AuthenticationFailed('Incorrect password!')

        # return JsonResponse({"massage":"its work"})
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        #print(token)
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        print(response)
        return response


class UserView(APIView):
    @csrf_exempt
    def get(self, request):
        # token = request.COOKIES.get('jwt')
        #
        # if not token:
        #     raise AuthenticationFailed('Unauthenticated!')
        #
        # try:
        #     print("yes")
        #     payload = jwt.decode(token, 'secret', 'HS256')
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=11).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

#
# class LogoutView(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             'message': 'success'
#         }
#         return response

#test done