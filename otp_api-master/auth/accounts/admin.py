from django.contrib import admin

from .models import UserModel,PhoneOtp
class UserModelAdmin(admin.ModelAdmin):
    list_display=['name','phone']


class PhoneOtpAdmin(admin.ModelAdmin):
    list_display=['phone','otp','count']


admin.site.register(PhoneOtp,PhoneOtpAdmin)
admin.site.register(UserModel,UserModelAdmin)
