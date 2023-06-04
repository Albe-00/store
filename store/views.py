from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from .models import Prodotto , Carrello , Ordine , ProdottoOrdine
from .forms import CreaNuovoProdotto



# Create your views here.

def home(response):
    return render(response, 'store/home.html', {})

def vetrina(response):
    return render(response, 'store/vetrina.html', {"prodottiInVendita":Prodotto.objects.all()})

def cliente(response):
    return render(response, 'store/cliente.html', {})

def nuovoProdotto(response):
    if response.method == "POST" :
        form = CreaNuovoProdotto(response.POST)
        
        if form.is_valid() :
            n = form.cleaned_data["nome"]
            d = form.cleaned_data["descrizione"]
            p = form.cleaned_data["prezzo"]
            nuovoP = Prodotto(nome=n, descrizione=d, prezzo=p)
            nuovoP.save()
            
            return HttpResponseRedirect("/vetrina") 
        
        else:
            print("form non valido")
            
    else :
        form = CreaNuovoProdotto()
        
    return render(response ,  "store/nuovoProdotto.html" , {"form":form})


def viewCarrello(response):
    if response.user.is_authenticated:
        carrelloCliente = Carrello.objects.filter(cliente=response.user)
        return render(response, 'store/carrello.html', {"carrelloCliente":carrelloCliente})
    else :
        return render(response, 'store/carrello.html', {})


def aggiungiAlCarrello(response):
    idProdotto = response.POST.get("idProdotto")
    quantita = response.POST.get("numeroPezzi")
    nuovoProdottoCarrello = Carrello(prodotto=Prodotto.objects.get(id=idProdotto), cliente=response.user, quantita=quantita)
    nuovoProdottoCarrello.save()
    
        
    return render(response ,  "store/vetrina.html" , {"prodottiInVendita":Prodotto.objects.all()})    
           
def revisioneOrdine(response):
    prodottiCarrello = Carrello.objects.filter(cliente=response.user)
    return render(response ,  "store/revisioneOrdine.html" , {"ordineDaRevisionare":prodottiCarrello})

def effettuaOrdine(response):
    nuovoOrdine = Ordine(cliente=response.user)
    nuovoOrdine.save()
    prodottiCarrello = Carrello.objects.filter(cliente=response.user)
    for prodottoCarrello in prodottiCarrello:
        nuovoProdottoOrdine = ProdottoOrdine(prodotto=prodottoCarrello.prodotto, ordine=nuovoOrdine, quantita=prodottoCarrello.quantita)
        nuovoProdottoOrdine.save()
        prodottoCarrello.delete()
    ordineDARevisionare = ProdottoOrdine.objects.filter(ordine=nuovoOrdine)    
    return render(response ,  "store/vetrina.html" , {})        
        
def pagamento(response):
    return render(response ,  "store/pagamento.html" , {})
    
        

    