from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
       

urlpatterns = [
    path('',views.index,name="taches"), 
    path('ajouter_tache',views.ajouter_tache,name="ajouter_tache"),
    path('tachestats',views.stats_tache,name="stats_tache"),
    path('tache_edit/<int:id>/', views.tache_edit, name='tache_edit'),
    path('tache_delete/<int:id>/', views.supprimer_tache, name='tache_delete'),
    path('search_tache/', csrf_exempt(views.search_tache), name='search_tache'),
    path('user_tache',views.profil,name="user_tache"),
    path('export_csv',views.export_csv,name="export_csv"),

]

