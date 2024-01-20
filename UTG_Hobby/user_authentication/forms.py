from django import forms


class OtpForm(forms.Form):
    email = forms.EmailField()