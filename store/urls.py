from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('cliente/', views.cliente, name='cliente'),    
    path('nuovoProdotto/', views.nuovoProdotto, name='nuovoProdotto'),
    path('vetrina',views.vetrina, name='vetrina'),
    path('carrello',views.viewCarrello, name='viewCarrello'),
    path('aggiungiAlCarrello',views.aggiungiAlCarrello, name='aggiungiAlCarrello'),
    path('revisioneOrdine',views.revisioneOrdine, name='revisioneOrdine'),
    path('effettuaOrdine',views.effettuaOrdine, name='effettuaOrdine'),
    path('pagamento',views.pagamento, name='pagamento'),
]



