from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Spécialité,Siege, Employé
from django.contrib import messages 
from django.shortcuts import redirect
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import csv
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Employé
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Employé, Spécialité, Siege
from taches.models import Taches
@login_required(login_url='/authent/login/')
def add_employé(request):
    spécialité = Spécialité.objects.all()
    siege = Siege.objects.all()

    if request.method == 'POST':
        cin = request.POST.get('cin')
        nom = request.POST.get('nom')
        prénom = request.POST.get('prénom')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        spécialité_name = request.POST.get('spécialité')
        siege_name = request.POST.get('siege')
        salair = request.POST.get('salair')
        nbr_taches = request.POST.get('nbr_taches')

        spécialité_obj = Spécialité.objects.get(name=spécialité_name)
        siege_obj = Siege.objects.get(name=siege_name)

        emp, created = Employé.objects.get_or_create(user=request.user)
        emp.cin=cin
        emp.nom=nom
        emp.prénom=prénom
        emp.phone=phone
        emp.email=email
        emp.adresse=adresse
        emp.spécialité=spécialité_obj.name 
        emp.siege=siege_obj.name 
        emp.salair=salair
        emp.nbr_taches=nbr_taches
        emp.save()
        return redirect('user_page')

    return render(request, 'employers/ajouter_employe.html', {
        'spécialité': spécialité,
        'siege': siege,
    })




@login_required(login_url='/authent/login/')
def search_employer(request):
    
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        employers = Employé.objects.filter(cin__istartswith=search_str) | Employé.objects.filter(nom__startswith=search_str) | Employé.objects.filter(spécialité__icontains=search_str)
        data = employers.values()
        return JsonResponse(list(data), safe=False)





@login_required(login_url='/authent/login/')
def index(request):
    spécialité = Spécialité.objects.all()
    siege = Siege.objects.all()
    employers = Employé.objects.order_by('nom')
    paginator = Paginator(employers,7)
    page_number=request.GET.get('page')
    page_obj=Paginator.get_page(paginator, page_number)
    context={
        'employers': employers,
        'page_obj': page_obj,
    }
    return render(request, 'employers/index.html', context)
@login_required(login_url='/authent/login/')
def ajouter_employe(request):
    spécialité = Spécialité.objects.all()
    employers = Employé.objects.all()
    siege = Siege.objects.all()

    context={
        'spécialité': spécialité,
        'siege' : siege,
        'employers': employers,
        'values': request.POST

    }
    if request.method == 'GET':
        return render(request, 'employers/ajouter_employe.html', context)
        
    
    

    
    if request.method == 'POST':
        cin = request.POST['cin']
        if not cin: 
            messages.warning(request,'Le champs CIN est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
    
        nom = request.POST['nom']
        if not nom: 
            messages.warning(request,'Le champs Nom est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
    
        prénom = request.POST['prénom']
        if not prénom: 
            messages.warning(request,'Le champs Prénom est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
        phone = request.POST['phone']
        if not phone: 
            messages.warning(request,'Le champs numéro de téléphone est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
        email = request.POST['email']
        if not email: 
            messages.warning(request,'Le champs adresse mail est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
        adresse = request.POST['adresse']
        if not adresse: 
            messages.warning(request,'Le champs adresse est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
        spécialité = request.POST['spécialité']
        if not spécialité: 
            messages.warning(request,'Le champs Spécialité est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
        siege = request.POST['siege']
        if not siege: 
            messages.warning(request,'Le champs Siege est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
        salair = request.POST['salair']
        if not salair: 
            messages.warning(request,'Le champs Salair est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)
        nbr_taches = request.POST['nbr_taches']
        if not nbr_taches: 
            messages.warning(request,'Le champs nombre des taches est neccessaire')
            return render(request, 'employers/ajouter_employe.html', context)

        Employé.objects.create(cin=cin, nom=nom, prénom=prénom, phone=phone, email=email, adresse=adresse, spécialité=spécialité, siege=siege, salair=salair, nbr_taches=nbr_taches)
        messages.success(request,'Employé enregistré avec succés')
        return redirect('employers')
@login_required(login_url='/authent/login/')
def employer_edit(request, id):
    employer = Employé.objects.get(pk=id)
    spécialité = Spécialité.objects.all()
    siege = Siege.objects.all()
    context ={
        'employer' : employer,
        'values' : employer,
        'spécialité': spécialité,
        'siege' : siege ,
        

    }
    if request.method == 'GET':
        
        return render(request, 'employers/employer_edit.html', context)
    if request.method == 'POST':
         cin = request.POST['cin']
         if not cin: 
            messages.warning(request,'Le champs CIN est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
    
         nom = request.POST['nom']
         if not nom: 
            messages.warning(request,'Le champs Nom est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
    
         prénom = request.POST['prénom']
         if not prénom: 
            messages.warning(request,'Le champs Prénom est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
         phone = request.POST['phone']
         if not phone: 
            messages.warning(request,'Le champs numéro de téléphone est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
         email = request.POST['email']
         if not email: 
            messages.warning(request,'Le champs adresse mail est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
         adresse = request.POST['adresse']
         if not adresse: 
            messages.warning(request,'Le champs adresse est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
         
         spécialité = request.POST['spécialité']
         if not spécialité: 
            messages.warning(request,'Le champs Spécialité est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
         siege = request.POST['siege']
         if not siege: 
            messages.warning(request,'Le champs Siége est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
         salair = request.POST['salair']
         if not salair: 
            messages.warning(request,'Le champs Salair est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
         nbr_taches = request.POST['nbr_taches']
         if not nbr_taches: 
            messages.warning(request,'Le champs nombre des taches est neccessaire')
            return render(request, 'employers/employer_edit.html', context)
        

         
         employer.cin=cin 
         employer.nom=nom
         employer.prénom=prénom
         employer.phone=phone
         employer.email=email
         employer.adresse=adresse
         employer.spécialité=spécialité
         employer.siege =siege
         employer.salair =salair
         employer.nbr_taches=nbr_taches
         employer.save()
         messages.success(request,'Modification enregistré avec succés')
         return redirect('employers')
@login_required(login_url='/authent/login/')
def home(request):
    donné = Employé.objects.all()
    infoges = Employé.objects.filter(spécialité = 'Informatique de Gestion').count()
    infoges =int(infoges)
    com = Employé.objects.filter(spécialité = 'Commerciale').count()
    com =int(com)
    pro = Employé.objects.filter(spécialité = 'Production').count()
    pro =int(pro)
    fin = Employé.objects.filter(spécialité = 'Finance').count()
    fin =int(fin)
    compt = Employé.objects.filter(spécialité = 'Comptabilité').count()
    compt =int(compt)
    rh = Employé.objects.filter(spécialité = 'Ressources Humaines').count()
    rh =int(rh)
    okh = Employé.objects.filter(siege = 'Om elkchab').count()
    okh =int(okh)
    mdh = Employé.objects.filter(siege = 'Mdhila').count()
    mdh =int(mdh)
    ked = Employé.objects.filter(siege = 'Metlaoui Kef Eddour').count()
    ked =int(ked)
    kfc = Employé.objects.filter(siege = 'Metlaoui Kefschfier').count()
    kfc =int(kfc)
    om = Employé.objects.filter(siege = 'Om laarayes').count()
    om =int(om)
    rdf = Employé.objects.filter(siege = 'Redeyef').count()
    rdf =int(rdf)

    special_list = ['Informatique de Gestion', 'Commerciale', 'Production', 'Finance', 'Comptabilité', 'Ressources Humaines']
    nomb_spec_list = [infoges, com, pro, fin, compt, rh]

    siege_list = ['Om elkchab', 'Mdhila', 'Metlaoui Kef Eddour', 'Metlaoui Kefschfier', 'Om laarayes', 'Redeyef']
    nomb_siege_list = [okh, mdh, ked, kfc, om, rdf]
    

    context = {
        'donné' : donné,
        'special_list' : special_list,
        'nomb_spec_list' : nomb_spec_list,
        'siege_list' : siege_list, 
        'nomb_siege_list' : nomb_siege_list,
    }
    return render(request, 'home.html', context)
@login_required(login_url='/authent/login/')
def supprimer_employer(request, id):
    employer = Employé.objects.get(pk=id)
    employer.delete()
    messages.success(request,'Employer supprimer avec succés')
    return redirect('employers')
@login_required(login_url='/authent/login/')
def stats(request):
    donné = Employé.objects.all()
    infoges = Employé.objects.filter(spécialité = 'Informatique de Gestion').count()
    infoges =int(infoges)
    com = Employé.objects.filter(spécialité = 'Commerciale').count()
    com =int(com)
    pro = Employé.objects.filter(spécialité = 'Production').count()
    pro =int(pro)
    fin = Employé.objects.filter(spécialité = 'Finance').count()
    fin =int(fin)
    compt = Employé.objects.filter(spécialité = 'Comptabilité').count()
    compt =int(compt)
    rh = Employé.objects.filter(spécialité = 'Ressources Humaines').count()
    rh =int(rh)
    okh = Employé.objects.filter(siege = 'Om elkchab').count()
    okh =int(okh)
    mdh = Employé.objects.filter(siege = 'Mdhila').count()
    mdh =int(mdh)
    ked = Employé.objects.filter(siege = 'Metlaoui Kef Eddour').count()
    ked =int(ked)
    kfc = Employé.objects.filter(siege = 'Metlaoui Kefschfier').count()
    kfc =int(kfc)
    om = Employé.objects.filter(siege = 'Om laarayes').count()
    om =int(om)
    rdf = Employé.objects.filter(siege = 'Redeyef').count()
    rdf =int(rdf)

    special_list = ['Informatique de Gestion', 'Commerciale', 'Production', 'Finance', 'Comptabilité', 'Ressources Humaines']
    nomb_spec_list = [infoges, com, pro, fin, compt, rh]

    siege_list = ['Om elkchab', 'Mdhila', 'Metlaoui Kef Eddour', 'Metlaoui Kefschfier', 'Om laarayes', 'Redeyef']
    nomb_siege_list = [okh, mdh, ked, kfc, om, rdf]
    

    context = {
        'donné' : donné,
        'special_list' : special_list,
        'nomb_spec_list' : nomb_spec_list,
        'siege_list' : siege_list, 
        'nomb_siege_list' : nomb_siege_list,
    }
    return render(request, 'employers/empstats.html',context)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Employé.csv'
    writer = csv.writer(response)
    writer.writerow(['CIN', 'Nom', 'Prénom', 'Spécialité', 'phone', 'email', 'siége'])
    employes = Employé.objects.all()
    for employe in employes:
        writer.writerow([employe.cin, employe.nom, employe.prénom, employe.spécialité, employe.phone, employe.email, employe.siege, employe.salair , employe.adresse , employe.nbr_taches , employe.occupe ])
    return response

def user_profile(request):
    user = request.user.id
    taches = Taches.objects.filter(employé=user)
    profile = Employé.objects.get(user=user)
    print(profile)
    context  ={
        'user' : user,
        'profile': profile,
        'taches':taches
    }
    print(context)

    return render(request, 'employers/user_page.html', context)

#current_user = request.user
    #employer = Employé.objects.filter(user = current_user ).count()
    #context = {
     #   'current_user' : current_user,
      #  'employer' : employer,

    #}
    #utilis = request.user.username
   # employe = Employé.objects.filter(user = utilis)
  #  context = {
 #       'employe' : employe,
#    }

