from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core import mail
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from gestiontache import settings
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import token_generator
from django.contrib.auth.decorators import login_required


# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email is use, chose an other one '}, status=409)
        
        
        
        
        return JsonResponse({'email_valid': True})
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username is use, chose an other one '}, status=409)
        
        
        
        
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request,'authent/register.html')
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.warning(request,'Password too short')
                    return render(request,'authent/register.html',)
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                messages.success(request,'Account Successfully created')
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))

                domain=get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64':uidb64, 'token' :token_generator.make_token(user)})
                activate_url='http://'+domain+link
                subject = 'Activate your account'
                message = 'Hi '+user.username+' Please use this link to activate your account\n' +activate_url
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]
                send_mail(subject, message, from_email, to_email , fail_silently=False)
                return render(request,'authent/register.html')
            
        return render(request,'authent/register.html')
class VerificationView(View):
    def get(self, request,uidb64,token):
        try:
            

            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)
            if not token_generator.check_token(user,token):
                return redirect('login'+'?message'+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            messages.success(request,'Account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass

        return redirect('login')
  
class LoginView(View):
    def get(self, request):
        return render(request,'authent/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user=auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome '+user.username+ ' you are now logged in')
                    return redirect('home')
                
                messages.error(request,'Account is not active, please check on your email')
                return render(request,'authent/login.html')
            messages.warning(request,'Invalid credentials, try again')
            return render(request,'authent/login.html')
        messages.warning(request,'Please fill all the fields')
        return render(request,'authent/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect('login')


    

    