from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    nome= forms.CharField(max_length=100)
    cognome= forms.CharField(max_length=100)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"] = self.fields.pop("nome")
        self.fields["last_name"] = self.fields.pop("cognome")
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name" , "email", "password1", "password2"]

