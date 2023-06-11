from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('cliente/', views.cliente, name='cliente'),    

    path('gestioneProdotti/', views.gestioneProdotti, name='gestioneProdotti'),
    path('nuovoProdotto/', views.nuovoProdotto, name='nuovoProdotto'), 
    path('modificaProdotto/', views.modificaProdotto, name='modificaProdotto'),
    path('eliminaProdotto/', views.nascondiProdotto, name='nascondiProdotto'),

    path('carrello',views.viewCarrello, name='viewCarrello'),
    path('aggiungiAlCarrello',views.aggiungiAlCarrello, name='aggiungiAlCarrello'),

    path('revisioneOrdine',views.revisioneOrdine, name='revisioneOrdine'),
    path('effettuaOrdine',views.effettuaOrdine, name='effettuaOrdine'),
    path('pagamento',views.pagamento, name='pagamento'),

    path('vediStoricoOrdini',views.vediStoricoOrdini, name='vediStoricoOrdini'),
    path('vediOrdine',views.vediOrdine, name='vediOrdine'),
]



