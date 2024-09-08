from django.shortcuts import render
from .models import Student,CustomUser,OTP
from .serializers import Studentserializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
import random
import requests
import json

# Create your views here.

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)  # Parse the JSON body
            print(data,"comes...")
            email = data.get("email")
            password = data.get("password")

            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"error": "User already exists"}, status=400)

            # Create new user
            user = CustomUser.objects.create_user(
                email=email,
                password=password  # Hash the password
            )
            otp=random.randint(100000,999999)
            OTP.objects.create(OTP=otp,email=email)

            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return JsonResponse(response_data, status=201)

        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return HttpResponse(status=405)  # Method not allowed for non-POST requests

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = data = JSONParser().parse(request)  # Parse the JSON body
            email = data.get("email")
            password = data.get("password")
            # Authenticate user
            user=CustomUser.objects.filter(email=email).first()
            if user and check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        
        except Exception as e:
            return JsonResponse({"error": f"{e} this is the issue"}, status=400)
    return HttpResponse(status=405)  # Method not allowed for non-POST requests


# OTP Template For Forgot OTP
def Forgot_otp(name, email, otp):
    url = "https://control.msg91.com/api/v5/email/send"
    payload = {
        'to': [{'name': name, 'email': email}],
        'from': {'name': 'pritimaya', 'email': 'support@clasoc.com'},
        'variables': {'name': name, 'OTP': otp},
        'domain': 'clasoc.com',
        'template_id': 'template_forgot_password'
    }
    payload = json.dumps(payload)
    headers = {
        "Content-Type": "application/JSON",
        "Accept": "application/json",
        "authkey": "396373AC78f3NtG6492a1a7P1"
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False


@csrf_exempt
def forgotpassword(request):
    if request.method=='POST':
        data = data = JSONParser().parse(request)  # Parse the JSON body
        email = data.get("email")
        user=CustomUser.objects.filter(email=email).first()
        if user:
            otp=random.randint(100000,999999)
            Forgot_otp('chiku',email,otp)
            return JsonResponse({"sucess": f"OTP:-{otp} "}, status=200)
        else:
           return JsonResponse({"error": "Invalid credentials"}, status=401)
    return HttpResponse(status=405)   

#forgot otp
@csrf_exempt
def forgot_otp_check(request):
    if request.method=='POST':
        data = data = JSONParser().parse(request)  # Parse the JSON body
        email = data.get("email")
        otp = data.get("OTP")
        password = data.get("password")
        otp_object=OTP.objects.filter(email=email).first()
        if otp_object:
            if otp_object.OTP==otp:
                user=CustomUser.objects.filter(email=email).first()
                user.set_password(password)
                user.save()
                otp_object.failed_attempts=0
                otp_object.OTP=random.randint(100000,999999)
                otp_object.save()
                return JsonResponse({'Sucess':"password set up"}, status=201)
            else:
                otp_object.failed_attempts+=1
                #reassign new otp after 3 failure attempt
                if otp_object.failed_attempts>=3:
                    otp_object.failed_attempts=0
                    otp_object.otp=random.randint(100000,999999)
                    otp_object.save()
                otp_object.save()
                return JsonResponse({"error": "Wrong OTP"}, status=401)
    return HttpResponse(status=405)


@csrf_exempt
def studentapi(request,pk):
    student=Student.objects.get(pk=pk)
    if request.method == 'GET':
        student=Student.objects.get(pk=pk)
        #convert to python
        serializer=Studentserializer(student)
        if serializer.validate:
            data=JSONRenderer().render(serializer.data)
            return HttpResponse(data,content_type="application/json")
        data=JSONRenderer().render(serializer.errors)
        return HttpResponse(data,content_type="application/json")
    
    if request.method == "POST":
        data=JSONParser().parse(request)
        print(data,type(data))
        serializer=Studentserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False)
        return JsonResponse(serializer.errors,safe=False)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Studentserializer(student, data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


