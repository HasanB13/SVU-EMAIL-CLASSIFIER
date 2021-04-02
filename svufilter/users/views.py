from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from classifier.models import Messages
from .models import mailModel
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from .form import RegisterForm, loginForm, TestMesaageForm, ChangePasswordForm
from classifier import views as clasViews
import imaplib
 
#Register function
def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            host = 'mail.svuonline.org'
            mail = imaplib.IMAP4_SSL(host,993)
            try:
                mail.login(username,password)
                emails = clasViews.GetAllMSG(username,password)
                user, created = User.objects.get_or_create(first_name=firstname, last_name=lastname, username=username)
                if created:
                    user.set_password(password)
                    user.save()
                    mailMod = mailModel(user=user,password=password)
                    mailMod.save()
                usr = User.objects.filter(username=username)
                idx = len(usr)-1
                usr = usr[idx]
                for i in range(len(emails['subject'])):
                    msg = Messages(subject=emails['subject'][i],content=emails['message'][i],date_get=emails['date'][i],typeEmail=emails['statue'][i],sender=emails['sender'][i],reciever=usr)
                    msg.save()
                messages.success(request,f'{username} Account created')
                return redirect('login')
            except:
                messages.error(request,f'Your Univirsity username or password wrong!')
                return redirect('register')
    else:
        form = RegisterForm()
    return render(request,'users/register.html',{'form':form})

def loginUser(request):
    if request.method=='POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(username,password)
            user = authenticate(request,username=username, password=password)
            print(user)
            if user:
                host = 'mail.svuonline.org'
                mail = imaplib.IMAP4_SSL(host,993)
                try:
                    mail.login(username,password)
                    mail.logout()
                    login(request,user)
                    return redirect('home')
                except:
                    messages.error(request,f'you change your SVU account password')
                    redirect('change_password')
            else:
                messages.error(request,f'your username or passowrd wrong')
                return redirect('login')
    else:
        form = loginForm()
        return render(request,'users/login.html',{'form':form})

def logoutUser(request):
    logout(request)
    return redirect('login')

def changePassword(request):
    if request.method == 'POST':
        username = request.user.username
        currentpassword = request.user.password
        form = ChangePasswordForm(request.POST)
        if form.is_valid:
            lastpassword = form.cleaned_data.get('lastpassword')
            newpassword = form.cleaned_data.get('newpassword')
            check = check_password(currentpassword,lastpassword)
            if check:
                u = User.objects.get(username=username)
                u.set_password(newpassword)
                u.save()
            else:
                messages.error(request,f'please enter your last password')
                return redirect('change_password')
    else:
        form=ChangePasswordForm()
        return render(request,'users/change_password.html',{'form':form})


def TestMsg(request):
    if request.method == 'POST':
        form = TestMesaageForm(request.POST)
        lst = []
        if form.is_valid():
            msg = form.cleaned_data['message']
            print(msg)
            lst.append(msg)
            statue = clasViews.classifier(lst)
            messages.success(request,'the message is {}'.format(statue[0]))
    
    form = TestMesaageForm()
    return render(request,'users/TestMsg.html',{'form':form})





