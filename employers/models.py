from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class Employé(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    cin=models.IntegerField(blank=True, null=True)
    nom=models.TextField(blank=True, null=True)
    prénom=models.TextField(blank=True, null=True)
    phone=models.PositiveIntegerField(blank=True, null=True)
    email=models.TextField(blank=True, null=True)
    adresse=models.TextField(blank=True, null=True)
    spécialité=models.CharField(max_length=266, blank=True, null=True)
    siege=models.CharField(max_length=266, blank=True, null=True)
    salair = models.PositiveIntegerField(blank=True, null=True)
    nbr_taches=models.PositiveIntegerField(blank=True, null=True)
    occupe = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)

class Spécialité(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class Siege(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name
'''
def create_employe(sender, instance, created, **kwargs):
    if created:
        Employé.objects.create(user=instance)
        print('Employé créer')
post_save.connect(create_employe, sender=User)
def update_employe(sender, instance, created, **kwargs):
    if created == False:
        instance.employe.save()
        print('Employé modifié')
post_save.connect(update_employe, sender=User)
'''
