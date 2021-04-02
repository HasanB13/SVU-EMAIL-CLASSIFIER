from django.shortcuts import render,HttpResponse, redirect
from .models import Messages
from django.contrib.auth.models import User
from users.models import mailModel
import imaplib
import email
from datetime import datetime
from django.contrib import messages as djangoMsg
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
import os
from users import views as usrviews
#import libraries of classifier model
import pickle
from sklearn.externals import joblib


#classifeir function
def classifier(msgs):
    ClassifierName = '/classifier.pkl'
    FittingName = '/datFit.pkl'
    clas = joblib.load(os.path.dirname(os.path.realpath(__file__)) + ClassifierName)
    fitt = joblib.load(os.path.dirname(os.path.realpath(__file__)) + FittingName)
    msgsFitting = fitt.transform(msgs)
    pred = clas.predict(msgsFitting)
    return pred

#Get all messages when register first time
def GetAllMSG(username,password):
    print("t1")
    host = 'mail.svuonline.org'
    mail = imaplib.IMAP4_SSL(host,993)
    
    emails = {
        'subject': [],
        'sender' : [],
        'date' : [],
        'message' : [],
        'statue' : []
    }
    #connect to the account
    try:
        mail.login(username,password)
        
        mail.select('INBOX')
        
        #Get all mails
        
        tmp , data = mail.search(None, '(ALL)')
        for num in data[0].split():
            tmp, data = mail.fetch(num, '(RFC822)')
            message = data[0][1].decode('utf-8')
            msg = email.message_from_string(message)
            Sender = msg['FROM']
            Sub = msg['SUBJECT']
            datet = msg["DATE"]
            DateMsg = datetime.strptime(datet[0:-6], '%a, %d %b %Y %H:%M:%S') 
            ll = ""
            body = ""
            messg = ""
            
            for subpart in msg.get_payload():
                body = body + str(subpart.get_payload(decode=True))+'\n'
            body = bytes(body,'utf-8').decode('unicode-escape')
            body = body[1:-1]
            for ch in body:
                messg+=ch
                if '''b'<div dir=''' in messg : break
            messg = messg[1:-13]
            
            emails['sender'].append(Sender)
            emails['subject'].append(Sub)
            emails['date'].append(DateMsg)
            emails['message'].append(messg)
        
        if len(emails['message'])>0:
            statueLst = classifier(emails['message'])
            for i in range(0,len(emails['message'])):
                emails['statue'].append(statueLst[i])
        else:
            print('you dont have any email') 

        
    except:
        pass
    return emails


#Get unSeen messages only
def GetUnseenMsg(username , password):
    host = 'mail.svuonline.org'
    mail = imaplib.IMAP4_SSL(host,993)
    emails = {
        'subject': [],
        'sender' : [],
        'date' : [],
        'message' : [],
        'statue' : []
    }
    #connect to the account
    try:
        mail.login(username,password)
        print('1')
    
        mail.select('INBOX')
        

        tmp , data = mail.search(None, '(UNSEEN)')
        for num in data[0].split():
            tmp, data = mail.fetch(num, '(RFC822)')
            message = data[0][1].decode('utf-8')
            msg = email.message_from_string(message)
            Sender = msg['FROM']
            Sub = msg['SUBJECT']
            datet = msg["DATE"]
            DateMsg = datetime.strptime(datet[0:-6], '%a, %d %b %Y %H:%M:%S') 
            ll = ""
            body = ""
            messg = ""
            
            for subpart in msg.get_payload():
                body = body + str(subpart.get_payload(decode=True))+'\n'
            body = bytes(body,'utf-8').decode('unicode-escape')
            body = body[1:-1]
            for ch in body:
                messg+=ch
                if '''b'<div dir=''' in messg : break
            messg = messg[1:-13]
            
            emails['sender'].append(Sender)
            emails['subject'].append(Sub)
            emails['date'].append(DateMsg)
            emails['message'].append(messg)
        if len(emails['message'])>0:
            statueLst = classifier(emails['message'])
            for i in range(0,len(emails['message'])):    
                emails['statue'].append(statueLst[i])
        else:
            print('you dont have new email') 
    except:
        pass

    return emails
    

@login_required
def home(request):
    print("1")
    username = request.user.username
    print(username)
    user = User.objects.filter(username=username)
    print(user)
    idx = len(user)-1
    emails = Messages.objects.filter(reciever=user[idx],typeEmail='ham')
    return render(request,'classifier/home.html',{'emails':emails})

def get_spam(request):
    username = request.user.username
    user = User.objects.filter(username=username)
    idx = len(user)-1
    emails = Messages.objects.filter(reciever=user[idx],typeEmail='spam')
    return render(request,'classifier/spam.html',{'emails':emails})

@login_required
def getNewMsg(request):
    username = request.user.username
    usernameid = request.user.id
    print(usernameid)
    user = User.objects.get(id=usernameid)
    print(user,"hasan")
    query = mailModel.objects.get(user_id=usernameid)
    print("q : ",query)
    password = query.password
    print(password,"pass")
    
    emails = GetUnseenMsg(username,password)
    print(len(emails))
    usr = User.objects.filter(username=username)
    print("R ",usr)
    idx = len(usr)-1
    usr = usr[idx]
    print(usr)
    for i in range(len(emails['subject'])):
        msg = Messages(subject=emails['subject'][i],content=emails['message'][i],date_get=emails['date'][i],typeEmail=emails['statue'][i],sender=emails['sender'][i],reciever=usr)
        msg.save()
    return redirect('home')

class MessagesDetailView(DetailView):
    model = Messages
