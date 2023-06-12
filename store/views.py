from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from .models import Prodotto , Carrello , Ordine , ProdottoOrdine
from .forms import *
from django.db.models import F,Sum,Q



# Create your views here.
def home(request):
    prodottiInVendita = Prodotto.objects.all()
    if request.method == "POST" :
        form = CercaProdotto(request.POST)
        
        if form.is_valid() :
            stringaRicerca = form.cleaned_data["stringaRicerca"]         

            prodottiTrovati = Prodotto.objects.filter(
                ( Q(nome__contains=stringaRicerca) | Q(descrizione__contains=stringaRicerca) ) & Q(visibile=True)
                )

            return render(request, 'store/home.html', {"form" : form , "prodottiTrovati":prodottiTrovati , "prodottiInVendita":prodottiInVendita})

        else:
            print("form non valido")
            
    else :
        form = CercaProdotto()
        return render(request ,  "store/home.html" , {"form":form , "prodottiInVendita":prodottiInVendita})

def cliente(response):
    return render(response, 'store/cliente.html', {})

def gestioneProdotti(request):

    prodottiSalvati = Prodotto.objects.all()

    if request.method == "POST" :

        idProdotto = request.POST.get("idProdotto")
        prodottoDaModificare = Prodotto.objects.get(id=idProdotto)

        if 'nuovoProdotto' in request.POST :
            return HttpResponseRedirect("/nuovoProdotto")

        if 'modificaProdotto' in request.POST :
                form = ModificaProdotto()
                return render(request, 'store/modificaProdotto.html', {"prodottoDaModificare" : prodottoDaModificare , "form" : form})

        if 'annullaModifiche' in request.POST :
            return render(request, 'store/gestioneProdotti.html', {"prodottiSalvati" : prodottiSalvati})

        if 'salvaModifiche' in request.POST:
            form = ModificaProdotto(request.POST)
            if form.is_valid():
                if form.cleaned_data["nuovoNome"] != "":
                    prodottoDaModificare.nome = form.cleaned_data["nuovoNome"]
                    print("nuovo nome: " + form.cleaned_data["nuovoNome"])
                if form.cleaned_data["nuovaDescrizione"] != "":
                    prodottoDaModificare.descrizione = form.cleaned_data["nuovaDescrizione"]

                if form.cleaned_data["nuovoPrezzo"] is not None:
                    prodottoDaModificare.prezzo = form.cleaned_data["nuovoPrezzo"]
                prodottoDaModificare.save()


            return render(request, 'store/gestioneProdotti.html', {"prodottiSalvati": prodottiSalvati})


        if 'modificaVisibilitaProdotto' in request.POST :

            if prodottoDaModificare.visibile == True :
                prodottoDaModificare.visibile = False
            else :
                prodottoDaModificare.visibile = True
            prodottoDaModificare.save()
            return render(request, 'store/gestioneProdotti.html', {"prodottiSalvati" : prodottiSalvati})

        return render(request, 'store/gestioneProdotti.html', {"prodottiSalvati" : prodottiSalvati})
    else:

        return render(request, 'store/gestioneProdotti.html', {"prodottiSalvati" : prodottiSalvati})
def nuovoProdotto(request):
    if request.method == "POST" :
        form = CreaNuovoProdotto(request.POST)
        
        if form.is_valid() :
            n = form.cleaned_data["nome"]
            d = form.cleaned_data["descrizione"]
            p = form.cleaned_data["prezzo"]
            nuovoP = Prodotto(nome=n, descrizione=d, prezzo=p)
            nuovoP.save()
            
            return HttpResponseRedirect("/home") 
        
        else:
            print("form non valido")
            
    else :
        form = CreaNuovoProdotto()
        
    return render(request ,  "store/nuovoProdotto.html" , {"form":form})



def gestioneAcquisto(request):
    if request.user.is_authenticated:
        if request.method == 'POST' :

            idProdotto = request.POST.get("idProdotto")
            quantita = request.POST.get("numeroPezzi")
            prodottoDaGestire = Prodotto.objects.get(id=idProdotto)
            if quantita == "":
                quantita = 1
            print("GESTIONE ACQUISTO")
            print("idProdotto: " + str(idProdotto))
            print("quantita: " + str(quantita))


            if 'acquistaOraButton' in request.POST :
                totale = prodottoDaGestire.prezzo * int(quantita)
                print("totale: " + str(totale))
                return render(request, "store/revisioneAcquistoRapido.html",{"prodottoDaRevisionare": prodottoDaGestire,"quantita":quantita ,"totale": totale})

            if 'aggiungiAlCarrelloButton' in request.POST :
                # Aggiungo il prodotto al carrello
                # se il prodotto è già nel carrello aggiungo la quantità senza aggiungere una nuova istanza
                for prodotto in Carrello.objects.filter(cliente=request.user):
                    if prodotto.prodotto.id == int(idProdotto):
                        prodotto.quantita += int(quantita)
                        prodotto.save()
                        return HttpResponseRedirect("/home")
                # altrimenti creo una nuova istanza
                nuovoProdottoCarrello = Carrello(prodotto=prodottoDaGestire, cliente=request.user,quantita=quantita)
                nuovoProdottoCarrello.save()
                return HttpResponseRedirect("/home")
    else:
        return HttpResponseRedirect("/login")

def aggiungiAlCarrello(request):
    if request.user.is_authenticated:
        idProdotto = request.POST.get("idProdotto")
        quantita = request.POST.get("numeroPezzi")
        if quantita == "":
            quantita = 1
        #se il prodotto è già nel carrello aggiungo la quantità senza aggiungere una nuova istanza
        for prodotto in Carrello.objects.filter(cliente=request.user):
            if prodotto.prodotto.id == int(idProdotto):
                prodotto.quantita += int(quantita)
                prodotto.save()
                return HttpResponseRedirect("/home")
        #altrimenti creo una nuova istanza
        nuovoProdottoCarrello = Carrello(prodotto=Prodotto.objects.get(id=idProdotto), cliente=request.user, quantita=quantita)
        nuovoProdottoCarrello.save()
    
        return HttpResponseRedirect("/home")    
    else:
        return HttpResponseRedirect("/login")

def viewCarrello(request):
    if request.user.is_authenticated:

        idProdotto = request.POST.get("idProdotto")
        if 'diminuisciQuantitaOggetto' in request.POST :
            prodottoDaModificare = Carrello.objects.get(id=idProdotto)
            prodottoDaModificare.quantita -= 1
            prodottoDaModificare.save()
            if prodottoDaModificare.quantita == 0 :
                prodottoDaModificare.delete()
                return HttpResponseRedirect("/carrello")
        if 'aumentaQuantitaOggetto' in request.POST :
            prodottoDaModificare = Carrello.objects.get(id=idProdotto)
            prodottoDaModificare.quantita += 1
            prodottoDaModificare.save()
        if 'rimuoviOggetto' in request.POST :
            prodottoDaModificare = Carrello.objects.get(id=idProdotto)
            prodottoDaModificare.delete()
            return HttpResponseRedirect("/carrello")

        carrelloCliente = Carrello.objects.filter(cliente=request.user).select_related('prodotto')
        totale = carrelloCliente.annotate(subtotale=F('quantita') * F('prodotto__prezzo')).aggregate(Sum('subtotale'))['subtotale__sum'] or 0
        return render(request, 'store/carrello.html', {"carrelloCliente": carrelloCliente, "totale": totale})
    else:
        return render(request, 'store/carrello.html', {})

def revisioneAcquistoRapido(request):
    if request.method == 'POST':
        idProdotto = request.POST.get("idProdotto")
        quantita = request.POST.get("quantita")
        prodottoDaGestire = Prodotto.objects.get(id=idProdotto)
        if 'diminuisciQuantitaOggetto' in request.POST:
            quantita = int(quantita) - 1
            if quantita == 0:
                return HttpResponseRedirect("/home")
        if 'aumentaQuantitaOggetto' in request.POST:
            quantita = int(quantita) + 1
        if 'rimuoviOggetto' in request.POST:
            return HttpResponseRedirect("/home")
        totale = prodottoDaGestire.prezzo * int(quantita)
        return render(request, "store/revisioneAcquistoRapido.html",{"prodottoDaRevisionare": prodottoDaGestire, "quantita": quantita, "totale": totale})

def effettuaAcquistoRapido(request):
    # Creo un nuovo ordine senza aggiungere il prodotto al carrello
    if request.method == 'POST':
        if 'effettuaAcquisto' in request.POST:
            idProdotto = request.POST.get("idProdotto")
            quantita = request.POST.get("quantita")
            prodottoDaGestire = Prodotto.objects.get(id=idProdotto)

            nuovoOrdine = Ordine(cliente=request.user)
            nuovoOrdine.save()
            nuovoProdottoOrdine = ProdottoOrdine(prodotto=prodottoDaGestire, ordine=nuovoOrdine, quantita=quantita)
            nuovoProdottoOrdine.save()
    return HttpResponseRedirect("/home")

def revisioneOrdine(request):
    if request.method == 'POST':    
        idProdotto = request.POST.get("idProdotto")
        if 'diminuisciQuantitaOggetto' in request.POST :
            prodottoDaModificare = Carrello.objects.get(id=idProdotto) 
            prodottoDaModificare.quantita -= 1
            prodottoDaModificare.save()
            if prodottoDaModificare.quantita == 0 :
                prodottoDaModificare.delete()
                return HttpResponseRedirect("/carrello")
        if 'aumentaQuantitaOggetto' in request.POST : 
            prodottoDaModificare = Carrello.objects.get(id=idProdotto) 
            prodottoDaModificare.quantita += 1
            prodottoDaModificare.save()
        if 'rimuoviOggetto' in request.POST : 
            prodottoDaModificare = Carrello.objects.get(id=idProdotto) 
            prodottoDaModificare.delete()
            return HttpResponseRedirect("/carrello")    

        
        prodottiCarrello = Carrello.objects.filter(cliente=request.user)
        totale = prodottiCarrello.annotate(subtotale=F('quantita') * F('prodotto__prezzo')).aggregate(Sum('subtotale'))['subtotale__sum'] or 0

        return render(request ,  "store/revisioneOrdine.html" , {"ordineDaRevisionare":prodottiCarrello , "totale": totale})

def effettuaOrdine(response):
    nuovoOrdine = Ordine(cliente=response.user)
    nuovoOrdine.save()
    prodottiCarrello = Carrello.objects.filter(cliente=response.user)
    for prodottoCarrello in prodottiCarrello:
        nuovoProdottoOrdine = ProdottoOrdine(prodotto=prodottoCarrello.prodotto, ordine=nuovoOrdine, quantita=prodottoCarrello.quantita)
        nuovoProdottoOrdine.save()
        prodottoCarrello.delete()    
    return HttpResponseRedirect("/pagamento")        
        
def pagamento(response):
    return render(response ,  "store/pagamento.html" , {})

def vediStoricoOrdini(response):
    ordiniCliente = Ordine.objects.filter(cliente=response.user)
    return render(response ,  "store/vediStoricoOrdini.html" , {"ordiniCliente":ordiniCliente })

def vediOrdine(request):
    if request.method == 'POST':   
        idOrdine = request.POST.get("idOrdine")  
        ordineDaVedere = Ordine.objects.get(id=idOrdine)
        prodottiDellOrdine=ProdottoOrdine.objects.filter(ordine = idOrdine)    
        totale = prodottiDellOrdine.annotate(subtotale=F('quantita') * F('prodotto__prezzo')).aggregate(Sum('subtotale'))['subtotale__sum'] or 0

        return render(request ,  "store/vediOrdine.html" , {"ordineDaVedere": ordineDaVedere , "prodottiDellOrdine" : prodottiDellOrdine , "totale": totale})
    else:       
        return render(request ,  "store/vediOrdine.html" , { })
        

    