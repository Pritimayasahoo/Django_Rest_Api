from django.shortcuts import render
from .models import Student
from .serializers import Studentserializer
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.middleware.csrf import get_token
# Create your views here.

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

@csrf_protect
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


