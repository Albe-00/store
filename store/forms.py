from django import forms

class CreaNuovoProdotto(forms.Form):
    nome = forms.CharField(label="nome", max_length=200)
    descrizione = forms.CharField(max_length=400)
    prezzo = forms.FloatField()
 
