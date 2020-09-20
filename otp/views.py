from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserModel
import base64
from django.urls import reverse

class GetPhoneNumber(generic.CreateView):
    template_name = "form.html"
    model = UserModel
    fields = ["phonenumber"]
    def get_success_url(self, *args, **kwargs):
        return reverse("otp:OTP Gen",kwargs={"phone": self.object.phonenumber})

class GetKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "This is the random key"

class RegistereNumber(APIView):
    @staticmethod
    def get(request, phone):
        try:
            phonenumber = UserModel.objects.get(phonenumber=phone)
        except ObjectDoesNotExist:
            UserModel.objects.create(
                phonenumber=phone,
            )
            phonenumber = UserModel.objects.get(phonenumber=phone)
        phonenumber.counter += 1
        phonenumber.save()
        keygen = GetKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.HOTP(key)
        print("otp:" + OTP.at(phonenumber.counter))
        return Response("your otp was sent to the terminal", status=200)


    @staticmethod
    def post(request, phone):
        try:
            phonenumber = UserModel.objects.get(phonenumber=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)

        keygen = GetKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.HOTP(key)

        if OTP.verify(request.data,phonenumber.counter):
            phonenumber.isVerified = True
            phonenumber.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)
