from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('cliente/', views.cliente, name='cliente'),    

    path('gestioneProdotti/', views.gestioneProdotti, name='gestioneProdotti'),
    path('nuovoProdotto/', views.nuovoProdotto, name='nuovoProdotto'),

    path('gestioneAcquisto', views.gestioneAcquisto, name='gestioneAcquisto'),

    path('revisioneAcquistoRapido', views.revisioneAcquistoRapido, name='revisioneAcquistoRapido'),
    path('effettuaAcquistoRapido', views.effettuaAcquistoRapido, name='effettuaAcquistoRapido'),


    path('aggiungiAlCarrello',views.aggiungiAlCarrello, name='aggiungiAlCarrello'),
    path('carrello',views.viewCarrello, name='viewCarrello'),


    path('revisioneOrdine',views.revisioneOrdine, name='revisioneOrdine'),
    path('effettuaOrdine',views.effettuaOrdine, name='effettuaOrdine'),


    path('salvaPagamento',views.salvaPagamento, name='salvaPagamento'),


    path('vediStoricoOrdini',views.vediStoricoOrdini, name='vediStoricoOrdini'),
    path('vediOrdine',views.vediOrdine, name='vediOrdine'),
]



