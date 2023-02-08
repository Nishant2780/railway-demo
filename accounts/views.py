from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


import requests
def nse_demo(request):
    print("NISHANT")
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    headers = {'user-agent': 'my-app/0.0.1'}
    response = requests.get(url, headers=headers)
    data = response.json()
    timestamp = data['records']['timestamp']
    print(timestamp)
    return render(request, 'PcrStocks.html', {'timestamp': timestamp})

def home(request):
    return render(request, 'home.html')