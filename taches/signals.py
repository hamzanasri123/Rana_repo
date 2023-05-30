from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Taches
from employers.models import Employé


@receiver(pre_save, sender=Taches)
def pre_save_create_disp(sender, instance, **kwargs):
    obj = Employé.objects.get(user=instance.employé.user)
    obj.occupe = True
    obj.save()

