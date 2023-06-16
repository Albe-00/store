from django import forms

class CreaNuovoProdotto(forms.Form):
    nome = forms.CharField(label="nome", max_length=200)
    descrizione = forms.CharField(max_length=400)
    prezzo = forms.FloatField()
    categoria = forms.CharField(max_length=200)
    visibile = forms.BooleanField(required=False)

class ModificaProdotto(forms.Form):
    nuovoNome = forms.CharField(label="nome", max_length=200, required=False)
    nuovaDescrizione = forms.CharField(max_length=400, required=False)
    nuovoPrezzo = forms.FloatField(required=False)
    nuovaVisibile = forms.BooleanField(required=False)

class CercaProdotto(forms.Form):
    stringaRicerca = forms.CharField(label="", max_length=200)


