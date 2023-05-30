from django.utils import timezone

def update_task_status():
    from taches.models import Taches
    tasks = Taches.objects.filter(date_fin__lte=timezone.now().date())
    for task in tasks:
        if task.etat!='finished':
            task.etat = 'finished'
            task.save()
