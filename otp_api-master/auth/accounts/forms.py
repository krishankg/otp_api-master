from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UserModel

class LoginForm(forms.Form):
    phone-forms.IntegerField(label='Your Phone Number')
    password=forms.CharField(widget=forms.PasswordInput)

class VerifyForm(forms.Form):
    key=forms.IntegerField(label='Please Enter OTP here')


class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model=UserModel
        fields=('phone',)

    def clean_phone(self):
        phone=self.cleaned_data.get('phone')
        qs=UserModel.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("Phone is taken")
        return phone

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError('Password does not match.')
        return password2


class TempRegisterForm(forms.Form):
    phone=forms.IntegerField()
    otp=forms.IntegerField()


class SetPasswordForm(forms.Form):
    password=forms.CharField(label='Passwrod',widget=forms.PasswordInput)
    password2=forms.CharField(label="Password confirmation",widget=forms.PasswordInput)


class UserAdminCreationForm(forms.ModelForm):
    password1=forms.CharField(label="password 1",widget=forms.PasswordInput)
    password2=forms.CharField(label="password 2",widget=forms.PasswordInput)

    class Meta:
        model=UserModel
        fields=('phone',)

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError('Password does not match.')
        return password2

    def save(self,commit=True):
        user=super(UserAdminCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=UserModel
        fields=('phone','password','active','admin')


    def clean_password(self):

        return self.initial('password')
