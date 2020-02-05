from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions,status,generics
import random
from .serializers import CreateUserSerializer
from .models import UserModel,PhoneOtp
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login,authenticate
# Create your views here.
class ValidateOtp(APIView):
    def post(self,request,*args,**kwargs):
        phone_number=request.POST.get('phone',False)
        otp_sent=request.POST.get('otp',False)
        if phone_number and otp_sent:
            old=PhoneOtp.objects.filter(phone__iexact=phone_number)
            if old.exists():
                old=old.last()
                otp=old.otp
                if str(otp_sent)==str(otp):
                    old.validate_field=True
                    old.save()
                    return Response({'status':True,'detail':'Otp Matched...'})
        else:
            return Response({'wrong':'bad reqeusts.'})


class ValidatePhoneSendOtp(APIView):
    def post(self,request,*args,**kwargs):
        phone_number=request.POST.get('phone')
        if phone_number:
            phone=str(phone_number)
            user=UserModel.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'status':True,'detail':'phone number already exists.right now'})
            else:
                key=send_otp(phone)
                if key:
                    old=PhoneOtp.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old=old.last()
                        count=old.count
                        if count > 4:
                            return Response({'status':False,'detail':"Otp can't sent you exceed limit.Please contact cumstomer care."})
                        old.count=count+1
                        print(key)
                        old.otp=key
                        old.save()
                        return Response({'status':True,'details':'Otp send successfully.'})
                    else:
                        new=PhoneOtp.objects.create(phone=phone,otp=key)
                        new.save()
                        print("----------------------")
                        print(key)
                        print("-------------------")
                        return Response({'status':True,'details':'Otp send successfully.'})
                else:
                    return Response({'status':False,'detail':'Otp Sending Error'})
        else:
            return Response({'status':False,'detail':'Phone number does not send post.'})



def send_otp(phone):
    if phone:
        key=random.randint(999,9999)
        return key
    else:
        return False


class Register(APIView):
    def post(self,request,*args,**kwargs):
        phone=request.POST.get('phone',False)
        password=request.POST.get('password',False)
        if phone and password:
            old=PhoneOtp.objects.filter(phone__iexact=phone)
            if old.exists():
                old=old.first()
                validated=old.validate_field
                if validated:
                    temp_data={
                      'phone':phone,
                      'password':password
                    }
                    serializer=CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user=serializer.save()
                    old.delete()
                    return Response({'status':True,'detail':'Account Created..'})
                else:
                    return Response({'status':False,'detail':'Otp does not verified.first verified it.'})
            else:
                return Response({'status':False,'detail':'Please verifed first'})
        else:
            return Response({'status':False,'detail':'Both phone and password not send.'})


class LoginAPIView(APIView):
    permissions_classes=(permissions.AllowAny,)
    def post(self,request,format=None):
        serializer=serializers.LoginSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        login(request,user)
        return super(LoginAPIView,self).post(request,format=None)
