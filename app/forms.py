from sre_constants import CATEGORY
from django import forms
from django.contrib.auth.models import User
from .models import *

GENDER=(
    ("","---Select Gender---"),
    ("Female","Female"),
    ("Male","Male"),
    ("Other","Other"),
)

SECURITY=(
    ("","---Select the security question---"),
    ("1","In what city were you born?"),
    ("2","What is the name of your favorite pet?"),
    ("3","what is the name of your first school?"),
    ("4","what is your favorite food?"),
)

#<-----Admin Add Form----->#
class AdminUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}), required=True)

    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'password', 'confirm_password']

    def clean(self):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        cleaned_data=super(AdminUserForm, self).clean()
        username=cleaned_data.get('username')
        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")

        if len(username) < 8:
            self.add_error('username','Username length must be greater than 8 character.')
        if not any (char in special_characters for char in password):
            self.add_error('password','Password must contain at least one special Character.')

        if len(password)  < 8:
            self.add_error('password','Password length must be greater than 8 character.')
        if not any (char.isdigit() for char in password):
            self.add_error('password','Password must contain at least one digit.')
        if not any (char in special_characters for char in password):
            self.add_error('password','Password must contain at least one special Character.')

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not Match")

        return cleaned_data

class AdminExtraForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email ID'}), required=True)
    gender = forms.ChoiceField(choices=GENDER,widget=forms.Select(attrs={'class':'form-control'}), required=True)

    class Meta:
        model=Admin
        fields=['email', 'gender']

#<-----Visistor Signup Form----->#
class VisitorUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Conform Password'}), required=True)

    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'password', 'confirm_password']

    def clean(self):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        cleaned_data=super(VisitorUserForm, self).clean()
        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")
        username =cleaned_data.get('username')

        if len(username) < 8:
            self.add_error('username','Username length must be greater than 8 character.')
        if not any (char in special_characters for char in password):
            self.add_error('password','Password must contain at least one special Character.')

        if len(password)  < 8:
            self.add_error('password','Password length must be greater than 8 character.')
        if not any (char.isdigit() for char in password):
            self.add_error('password','Password must contain at least one digit.')
        if not any (char in special_characters for char in password):
            self.add_error('password','Password must contain at least one special Character.')

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not Match")

        return cleaned_data

class VisitorExtraForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email ID'}), required=True)
    gender = forms.ChoiceField(choices=GENDER,widget=forms.Select(attrs={'class':'form-control'}), required=True)

    class Meta:
        model=Visitor
        fields=['email', 'gender']

#<-----Visistor Login Form----->#
class VisitorLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}), required=True)

#<-----Seller Login Form----->#
class SellerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}), required=True)

#<-----Admin Login Form----->#
class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}), required=True)



#<-----Find Crop Form----->#
class FindCropForm(forms.Form):
    nitrogen = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter level of Nitrogen'}), required=True)
    phosphorus = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter level of Phosphorus'}), required=True)
    potassium = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter level of Potassium'}), required=True)
    temperature = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Temperature (in Celsius)'}), required=True)
    humidity = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Humidity'}), required=True)
    ph = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter pH value'}), required=True)
    rainfall = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Rainfall (in cm)'}), required=True)
