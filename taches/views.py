from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.shortcuts import redirect
from .models import  Taches, Etat
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import csv
from employers.models import Employé


# Create your views here.
@login_required(login_url='/authent/login/')
def search_tache(request):
    
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        taches = Taches.objects.filter(nom__startswith=search_str) | Taches.objects.filter(etat__icontains=search_str) | Taches.objects.filter(date_debut__startswith=search_str) | Taches.objects.filter(date_fin__startswith=search_str)
        data = taches.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authent/login/')
def index(request):
    #etat = Etat.objects.all()
    taches = Taches.objects.order_by('nom')
    paginator = Paginator(taches,7)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator, page_number)
    context={
        'taches': taches,
        'page_obj': page_obj,
    }
    return render(request, 'taches/index.html', context)
@login_required(login_url='/authent/login/')
def ajouter_tache(request):
    etat = Etat.objects.all()
    taches = Taches.objects.all()
    employe = Employé.objects.all()
   

    context={
        'etat': etat,
        'taches': taches,
        'employe' : employe,
        'values': request.POST

    }
    if request.method == 'GET':
        return render(request, 'taches/ajouter_tache.html', context)
        
    
    

    
    if request.method == 'POST':
        nom = request.POST['nom']
        if not nom: 
            messages.warning(request,'Le champs Nom est neccessaire')
            return render(request, 'taches/ajouter_tache.html', context)
    
        description = request.POST['description']
        if not description: 
            messages.warning(request,'Le champs Description est neccessaire')
            return render(request, 'taches/ajouter_teche.html', context)
        montant = request.POST['montant']
        if not montant: 
            messages.warning(request,'Le champs Besoins financier de la tâche est neccessaire')
            return render(request, 'taches/ajouter_teche.html', context)
    
        etat = request.POST['etat']
        if not etat: 
            messages.warning(request,'Le champs Etat est neccessaire')
            return render(request, 'taches/ajouter_tache.html', context)
        date_debut = request.POST['date_debut']
        if not date_debut: 
            messages.warning(request,'Le champs Date Début est neccessaire')
            return render(request, 'taches/ajouter_tache.html', context)
        date_fin = request.POST['date_fin']
        if not date_fin: 
            messages.warning(request,'Le champs Date Fin est neccessaire')
            return render(request, 'taches/ajouter_tache.html', context)
        employe = request.POST['employe']
        if not employe: 
            messages.warning(request,'Le champs Employé est neccessaire')
            return render(request, 'taches/ajouter_tache.html', context)

        

        Taches.objects.create(nom=nom, description=description, montant=montant, etat=etat, date_debut=date_debut, date_fin=date_fin, employe=employe)
        messages.success(request,'Tache enregistré avec succés')
        return redirect('taches')
@login_required(login_url='/authent/login/')
def tache_edit(request, id):
    taches = Taches.objects.get(pk=id)
    etat = Etat.objects.all()
    context ={
        'taches' : taches,
        'values' : taches,
        'etat': etat,

    }
    if request.method == 'GET':
        
        return render(request, 'taches/tache_edit.html', context)
    if request.method == 'POST':
         nom = request.POST['nom']
         if not nom: 
            messages.warning(request,'Le champs Nom est neccessaire')
            return render(request, 'taches/tache_edit.html', context)
    
         description = request.POST['description']
         if not description: 
            messages.warning(request,'Le champs Description est neccessaire')
            return render(request, 'taches/tache_edit.html', context)
         montant = request.POST['montant']
         if not montant: 
            messages.warning(request,'Le champs Besoins financier de la tâche est neccessaire')
            return render(request, 'taches/tache_edit.html', context)
    
         etat = request.POST['etat']
         if not etat: 
            messages.warning(request,'Le champs Etat est neccessaire')
            return render(request, 'taches/tache_edit.html', context)
         date_debut = request.POST['date_debut']                                      
         if not date_debut: 
            messages.warning(request,'Le champs Date Début est neccessaire')
            return render(request, 'taches/tache_edit.html', context)
         date_fin = request.POST['date_fin']
         if not date_fin: 
            messages.warning(request,'Le champs Date FIN est neccessaire')
            return render(request, 'taches/tache_edit.html', context)
         taches.nom=nom
         taches.description=description
         taches.montant =montant
         taches.etat= etat
         taches.date_debut=date_debut
         taches.date_fin=date_fin
         taches.save()
         messages.success(request,'Modification enregistré avec succés')
         return redirect('taches')
@login_required(login_url='/authent/login/')
def supprimer_tache(request, id):
    taches = Taches.objects.get(pk=id)
    taches.delete()
    messages.success(request,'Tache supprimer avec succés')
    return redirect('taches')
@login_required(login_url='/authent/login/')
def stats_tache(request):
    taches = Taches.objects.all()
    trm = Taches.objects.filter(etat = 'finished').count()
    trm =int(trm)
    rep = Taches.objects.filter(etat = 'Reportée').count()
    rep =int(rep)
    ann = Taches.objects.filter(etat = 'Annulée').count()
    ann =int(ann)
    enc = Taches.objects.filter(etat = 'En Cours').count()
    enc =int(enc)
    att = Taches.objects.filter(etat = 'started').count()
    att =int(att)
    etat_list = ['finished', 'Reportée', 'Annulée', 'En Cours', 'started']
    nomb_etat_list = [trm, rep, ann, enc, att]
    context = {
        'taches' : taches,
        'etat_list' : etat_list,
        'nomb_etat_list' : nomb_etat_list,

        
    }
    return render(request, 'taches/tachestats.html',context)
def profil(request):
    

    # premiére
    #current_user = request.user
    #tch = Taches.objects.filter(employé = current_user)
    #context = {
     #   'current_user' : current_user,
      #  'tch' : tch,
    #}
    # deuxiéme 
    #current_user = request.user
    #user_name = current_user.cin
    #print(user_name)
    #context = {
     #   'user_name' : user_name,

    #}
    return render(request, 'user_tache.html')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Tache.csv'
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Description', 'Montant', 'Etat', 'Date début', 'Date fin', 'Employé'])
    taches = Taches.objects.all()
    for tache in taches:
        writer.writerow([tache.nom, tache.description, tache.montant, tache.etat, tache.date_debut, tache.date_fin, tache.employé])
    return response