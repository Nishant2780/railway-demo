from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    headers = {'user-agent': 'my-app/0.0.1'}
    response = requests.get(url, headers=headers)
    data = response.json()
    timestamp = data['records']['timestamp']
    summ = data['filtered']['CE']['totOI']
    summ2 = data['filtered']['PE']['totOI']
    pcr = summ2 / summ
    return render(request, 'PcrStocks.html', {'timestamp': timestamp, 'pcr': pcr})

def home(request):
    return render(request, 'home.html')


@api_view(['GET'])
def pcrstockput(request):

    baseurl = "https://www.nseindia.com/"
    headers =  {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                        'like Gecko) '
                        'Chrome/80.0.3987.149 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    req = session.get(baseurl, headers=headers, timeout=5)
    cookies = dict(req.cookies)
    stock = 'IPCALAB'
    
    url = 'https://www.nseindia.com/api/option-chain-equities?symbol=' + stock

    response = requests.get(url, headers=headers, timeout=5, cookies=cookies)
    data = response.text
    api_data = json.loads(data)
    time_stamp = api_data['records']['timestamp']
    livePrice = api_data['records']['underlyingValue']
    filteredData = api_data['filtered']['data']

    summ = api_data['filtered']['CE']['totOI']
    summ2 = api_data['filtered']['PE']['totOI']
    pcr = '%.2f'% (summ2 / summ)

    down_price = []
    down__price = api_data['filtered']['data']
    for down in down__price:
        if down['strikePrice'] <= livePrice:
            down_price.append(down)
    
    up_price = []
    up__price = api_data['filtered']['data']
    for up in up__price:
        if up['strikePrice'] >= livePrice:
            up_price.append(up) 

    # livePrice = { 'livePrice': livePrice}

    main_data = {"time_stamp": time_stamp,"livePrice": livePrice, 'pcr':pcr, 'down_price':down_price, 'up_price': up_price}
    return Response({ 'status' : True, 'msg' : 'success data', 'data' : main_data })

