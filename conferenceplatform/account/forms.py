from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class ChangePasswordForm(forms.Form):
    username = forms.CharField()
    old_password = forms.CharField()
    new_password = forms.CharField()
    confirm_password = forms.CharField()

class NormalUserRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()

class OrganizationUserRegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    org_name = forms.CharField()
    department = forms.CharField()
    contacts = forms.CharField()
    phone_number = forms.CharField()
    address = forms.CharField()
    bussiness_license = forms.FileField()
    id_card_front = forms.FileField()
    id_card_reverse = forms.FileField()

class OrganizationSubUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()