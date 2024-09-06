from django.shortcuts import render
from .models import Student,CustomUser
from .serializers import Studentserializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


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


