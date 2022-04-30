from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re

from station_admin.models import UserProfile


class SignupForm(UserCreationForm):
    # email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=25)

    def clean_phone_number(self) -> str:
        phone_number = self.cleaned_data['phone_number']
        if not re.match("^(\+3706)\d{7}$", phone_number):
            raise forms.ValidationError('Phone number format incorrect. Must start with +3706')
        elif not len(UserProfile.objects.filter(phone_number=phone_number)) == 0:
            raise forms.ValidationError('This phone number is already used')

        return phone_number


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number')
