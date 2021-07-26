from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .dataverifier import *
from django.http import JsonResponse as Response
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
# Create your views here.

# check request.method==post -> to be add



@csrf_exempt
def genrateotp(request):
    if not request.method == "POST":
        return Response({'status':404,'message':'NOT FOUND.'})
    try:
        email = json.loads(request.body).get("email")
        mail_status,mail_message = isvalidemail(email)
        if not mail_status:
            return Response({'status':400,'message':mail_message})
    except:
        return Response({'status':404,'message':'Please provide email.'})
    otp = randomotpgen()
    r1,messgae = islimitdone(email)
    if r1:
        output = sendmail(to=email,otp=otp)
        if output == 'success':
            return Response({'status':200,'message':'Success'})
        return Response({'status':500,'message':output})
    else:
        return Response({'status':400,'message':messgae})


def loginuser(request):
    if not request.method == "POST":
        return redirect('/')
    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except:
        return redirect('/')
    user = authenticate(username=username,password=password)
    if user is None:
        return HttpResponse({'Invalid credentials.'})
    else:
        login(request,user)
        return redirect('/')


def signupuser(request):
    if not request.method == "POST":
        return redirect('/')
    try:
        username = request.POST["username"]
        email = username
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        otp = request.POST["otp"]
    except:
        return redirect('/')
    
    val,mail_status = isvalidemail(email)
    # print(mail_status)
    if not val:
        return HttpResponse({mail_status})

    value,pass_status = passwordManager(password,cpassword)
    # print(pass_status)
    if not value:
        return HttpResponse({pass_status})

    mail_val,mail_status1 = preprocessmail(email)
    # print(mail_status1)
    if not mail_val:
        return HttpResponse({mail_status1})

    otp_val,otp_status = otp_match(otp,email)
    # print(otp_status)
    if not otp_val:
        return HttpResponse({otp_status})
    retuser,retcum = savemodels(email,password)
    
    user = authenticate(username=username,password=password)
    login(request,user)
    
    return redirect('/')


def logoutuser(request):
    logout(request)
    return redirect('/')


def claim_reward(request):
    if not request.user.is_authenticated:
        return redirect('/')
    user = request.user
    obj = cum.objects.get(index=user)
    if obj.last_reward_claimed != timezone.now().date():
        obj.last_reward_claimed = timezone.now().date()
        obj.nested_balance += 0.01
        obj.save()
        return Response({'status':200,'message':'Reward claimed successfully','credits':obj.nested_balance})
    return Response({'status':404,'message':'Already claimed reward for today.','credits':obj.nested_balance})