from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .dataverifier import *
from django.http import JsonResponse as Response
import json
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
# Create your views here.




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
    retuser = savemodels(email,password)
    
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
    obj = User.objects.get(email=user.email)
    if obj.last_reward_claimed != timezone.now().date():
        obj.last_reward_claimed = timezone.now().date()
        obj.nested_balance += 0.01
        obj.save()
        return Response({'status':200,'message':'Reward claimed successfully','credits':obj.nested_balance})
    return Response({'status':404,'message':'Already claimed reward for today.','credits':obj.nested_balance})



@csrf_exempt
def forgetpassgen(request):
    if request.method != "POST":
        return Response({'status':400,'message':'Invalid Request.'})
    try:
        email = json.loads(request.body).get("email")
    except:
        return Response({'status':400,'message':'Invalid Request.'})
    
    try:
        User.objects.get(email=email)
    except:
        return Response({'status':404,'message':'User not found.'})
    otp = randint(100000,999999)
    try:
        obj = TPS.objects.get(email=email)
        send_time = obj.send_at
        cur_time = timezone.now()
        del_time = str(cur_time-send_time)
        print(del_time)
        hours,minutes,seconds = map(float,del_time.split(':'))
        if int(hours)!=0:
            generate_and_savefp(email,otp)
        if int(minutes)<=5:
            return Response({'status':206,'message':'OTP send please retry after 5 minutes.'})
        generate_and_savefp(email,otp)
    except Exception as e:
        generate_and_savefp(email,otp)

    status = sendmail(to=email,subject="Password Change Attempt on cbv2.com",otp=otp,bypass_auth=True,store_data=False)

    return Response({'status':200,'message': status})


@csrf_exempt
def final_save_fp(request):
    if request.method != "POST":
        return Response({'status':400,'message':'Invalid Request.'})
    body = json.loads(request.body)
    try:
        email = body.get("email")
        otp = body.get("otp")
        password = body.get("password")
        cpassword = body.get("cpassword")
    except:
        return Response({'status':400,'message':'Invalid Request'})

    try:
        obj = TPS.objects.get(email=email)
        del_time = str(timezone.now() - obj.send_at)
        hour,minute,second = del_time.split(':')
        status,msg = passwordManager(password,cpassword)
        if not status:
            return Response({'status':406,'message':msg})
        if int(obj.otp) != int(otp.strip()):
            return Response({'status':406,'message':'Invalid OTP.'})
        if hour != 0 or minute <= 5:
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
            except:
                return Response({'status':403,'message':'Can not find user.'})
    except:
        return Response({'status':500,'message':'something went wrong.'})
    try:
        TPS.objects.get(email=email).delete()
    except:
        pass
    return Response({'status':'200','message':'success'})