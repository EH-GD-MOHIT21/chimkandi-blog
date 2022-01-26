import smtplib
from email.message import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from random import randint
from .models import Temporarystorage as TPS
from django.utils import timezone
from blogAPP.models import *
from .models import User


def phoneverifier(phone):
    if len(phone)!=10 or not(phone.isnumeric()):
        return False
    return True


def verifyname(name):
    if len(name) < 4:
        return False
    name = name.split(' ')
    for n in name:
        if not n.isalpha():
            return False
    return True

def preprocessmail(mail):
    if mail.count('@')!=1:
        return (False,"Invalid Mail Id")
    if len(mail)<5:
        return (False,"Invalid mail id")
    try:
        User.objects.get(email=mail)
        return (False,"Mail id already exists")
    except:
        pass
    try:
        obj = TPS.objects.get(email=mail)
        send_time = obj.send_at
        cur_time = timezone.now()
        del_time = str(cur_time-send_time)
        hours,minutes,seconds = map(float,del_time.split(':'))
        if int(hours)!=0:
            return (False,"Otp Expired")
        if int(minutes)<=5:
            return (True,None)
        return (False,"Otp Expired")
    except:
        return (False,"Please Generate Otp")


def passwordManager(p1,p2):
    if len(p1)<8:
        return (False,"Minimum length should be 8 for password")
    if p1!=p2:
        return (False,"Both Password didnot match")
    if p1.isnumeric() or p1.isalpha() or p1.isalnum():
        return (False,"use number alphabets and special chars in password")
    return (True,None)


def otpmatch(original,submitted):
    return original==submitted


def verifyAge(age):
    try:
        age = int(age)
        if age > 8 and age <= 120:
            return True
        else:
            return False
    except:
        return False

def isvalidemail(mail):
    if mail.count('@')!=1:
        return (False,"Invalid Mail id")
    if len(mail)<5:
        return (False,"Invalid Mail id")
    try:
        User.objects.get(email=mail)
        return (False,"Mail id already exists")
    except:
        pass
    return (True,None)

@csrf_exempt
def sendmail(to,request=None,subject=None,messageper=None,otp=None,bypass_auth=False,store_data=True):
    message = EmailMessage()
    message['To'] = to
    if not bypass_auth:
        value,status = isvalidemail(to)
        if not value:
            return status
    if subject!=None:
        message['Subject'] = subject
    else:
        message['Subject'] = "Welcome to NestedForms.com"
    message['From'] = settings.EMAIL_SENDER
    if messageper==None:
        message.set_content(f"Hello User welcome to ChimkandiBlogs.com Your one time password is {otp} valid for 5 minutes.\n\n\n Happy Form Bloging.\n Regards\n ChimkandiBlogs.com")
    else:
        message.set_content(messageper)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL_SENDER, settings.PASS_SENDER)
        server.send_message(message)
        if store_data:
            store_at = TPS(email=to,otp=otp)
            store_at.timestampnow
            store_at.save()
        return 'success'
    except Exception as e:
        print(e)
        return 'Email Not send.'

def randomotpgen():
    return randint(100000,999999)

def islimitdone(email):
    try:
        User.objects.get(username=email)
        return (False,"Mail id Already Exists")
    except Exception as e:
        # print(e)
        pass
    try:
        obj = TPS.objects.get(email=email)
        send_time = obj.send_at
        cur_time = timezone.now()
        del_time = str(cur_time-send_time)
        hours,minutes,seconds = map(float,del_time.split(':'))
        if int(hours)!=0:
            obj.delete()
            return (True,None)
        if int(minutes)>=5:
            obj.delete()
            # delete record
            return (True,None)
        return (False,'Otp has been send please try again 5 minutes.')
    except:
        return (True,None)

def otp_match(otp,email):
    try:
        obj = TPS.objects.get(email=email)
        if str(otp)!= str(obj.otp):
            return (False,"Otp Didn't Match")
        else:
            obj.delete()
            return (True,None)
    except:
        return (False,"Please Generate Otp to evaluate")


def savemodels(email,passwd):
    user = User(email=email)
    user.set_password(passwd)
    user.nested_balance = 1.0
    user.reward
    user.save()
    return (user)


def generate_and_savefp(email,otp):
    try:
        TPS.objects.get(email=email).delete()
    except:
        pass
    store_at = TPS(email=email,otp=otp)
    store_at.timestampnow
    store_at.save()