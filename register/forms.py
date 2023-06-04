from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    nome= forms.CharField(max_length=100)
    cognome= forms.CharField(max_length=100)
    email = forms.EmailField()

    #FIXME correggere la registrazione , aggiungendo nome e cognome
    #con questo dico di salvare nel database username
    #quando salveremo qualcosa in questo form verra salvato in username
    
    class Meta:
        model = User
        fields = ["username", "nome" , "cognome" , "email", "password1", "password2"]

