from django.urls import path, include
from .views import RegistereNumber,GetPhoneNumber

app_name="otp" 
urlpatterns = [
    path("<phone>/", RegistereNumber.as_view(), name="OTP Gen"),
    path("",GetPhoneNumber.as_view(),name = "Get Num")
]
