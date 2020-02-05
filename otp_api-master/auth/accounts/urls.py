from django.urls import path

from . import views

app_name='accounts'

urlpatterns=[
     path('hello/',views.ValidatePhoneSendOtp.as_view(),name='api'),
     path('validate/',views.ValidateOtp.as_view(),name='validate_api'),
     path('register/',views.Register.as_view(),name='register'),
]
 
