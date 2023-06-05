from email import message
import email
from django.contrib import messages,auth
from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import Account
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_no']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.save()
            user.phone_number=phone_number
            # messages.success(request,'Registeration Hora Hai')
            # return redirect('register')
            current_site=get_current_site(request)
            mail_subject="GreatKart: Activate your account"
            message=render_to_string('accounts/verification.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
            return redirect('register')

    else:
         form=RegistrationForm()

    context={
            'form':form,
        }

    return render(request,'accounts/register.html',context)

def activate(request,uidb64,token):
    uid=urlsafe_base64_decode(uidb64).decode()
    user=Account._default_manager.get(pk=uid)


    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulation your acc has been activated")
        return redirect('login')
    else:
        messages.error(request,"Invalid Activation link")
        return redirect('register')


def login(request):
    if request.method=='POST':
        email=request.POST.get('email')

        password=request.POST.get('password')
        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'Login Successful')
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')


def logout(request):
    auth.logout(request)
    messages.success(request,"You are successfully logged out")
    return redirect('login')

def forgot_pass(request):
    if request.method=="POST":
        email=request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="Reset your password"
            message=render_to_string('accounts/forgot_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()

            messages.success(request,"Password reset email has been sent")
            return redirect('login')
        else:
            messages.error(request,"Account does not exist")
            return redirect('forgot_pass')
    return render(request,'accounts/forgot_pass.html')


def resetpassword(request,uidb64,token):
    uid=urlsafe_base64_decode(uidb64).decode()
    user=Account._default_manager.get(pk=uid)


    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"please reset your password")
        return redirect('reset')
    else:
        messages.error(request,"this link has been expired")
        return redirect('register')

def reset(request):
    if request.method=='POST':
        password=request.POST.get('password')

        cpassword=request.POST.get('cpassword')
        if password==cpassword:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Your password has been reset')
            return redirect('login')
        else:
            messages.error(request,'Password does not match')
            return redirect('resetpassword')

    else:
        return render(request,'accounts/reset.html')

    
