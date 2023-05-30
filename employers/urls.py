from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
       

urlpatterns = [
    path('',views.index,name="employers"), 
    path('ajouter_employe',views.add_employé,name="ajouter_employe"),
    path('empstats',views.stats,name="stats"),
    path('employer_edit/<int:id>/', views.employer_edit, name='employer_edit'),
    path('employer_delete/<int:id>/', views.supprimer_employer, name='employer_delete'),
    path('search_employer/', csrf_exempt(views.search_employer), name='search_employer'),
    path('export_csv',views.export_csv,name="export_csv_emp"),
    path('user_page',views.user_profile,name="user_page"),
    path('home/', views.home, name='home'),

]



