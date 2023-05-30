from django.db import models
from employers.models import Employé
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

class Taches(models.Model):
    nom = models.TextField()
    description = models.TextField()
    montant = models.PositiveIntegerField(null=True)
    etat = models.CharField(max_length=266,default="started")
    date_debut = models.DateField()
    date_fin = models.DateField()
    employé = models.ForeignKey(Employé,null=True, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        self.send_email_to_employé()
        super().save(*args, **kwargs)
    def send_email_to_employé(self):
        if self.etat=="started":
            subject = 'New Task Assigned'
            message = f'Hello {self.employé.user.username},\n\nYour task {self.nom}'
        else:
            subject = 'Task Finished'
            message = f'Hello {self.employé.user.username},\n\nYour task {self.nom} has been finished'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.employé.user.email, ]
        send_mail(subject, message, email_from, recipient_list)
    

    def __str__(self):
        return self.nom 
    class Meta:
        ordering = ['-date_debut']
class Etat(models.Model):
    name = models.CharField(max_length=255, null=True)


    def __str__(self):
        return self.name
