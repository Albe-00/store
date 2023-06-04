from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Prodotto(models.Model):
    nome = models.CharField(max_length=200)
    descrizione = models.CharField(max_length=400)
    prezzo = models.FloatField()
    #TODO manca il collegamento con il tag e la categoria

    def __str__(self):
        return self.nome+" | "+self.descrizione+" , prezzo : "+str(self.prezzo) +" €"


#Classe di associazione tra prodotto e carrello con la quantità    
class Carrello(models.Model):
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    quantita = models.IntegerField()

    def __str__(self):
        return "carrello di "+ str(self.cliente)+" : "+str(self.prodotto)+", numero pezzi : "+str(self.quantita)


class Ordine(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE , null=False)

    def __str__(self):
        return "ordine di "+self.cliente.username+" | "+str(self.id)


#Classe di associazione tra prodotto e ordine con la quantità  
class ProdottoOrdine(models.Model):
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE)
    quantita = models.IntegerField()

    def __str__(self):
        return str(self.ordine)+" : "+str(self.prodotto)+", numero pezzi : "+str(self.quantita)

    
    
