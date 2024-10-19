from django.shortcuts import render
from .models import Student,CustomUser,OTP,Profile,Followerscount,Like_post,Comment,Post
from .serializers import Studentserializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.db.models import Q
import random
import requests
import json

# Create your views here.

#Default images
default_image = 'default.png'
default_cover_image ='default_cover_img.png'

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
            Profile.objects.create(user=user,id=user.id)
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


def logout_view(request):
    jwt_auth = JWTAuthentication()

    # Extract the access token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JsonResponse({"error": "Access token missing"}, status=400)

    try:
        # JWTAuthentication expects 'Bearer <access_token>' format
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)

        # Optional: Blacklist the refresh token if provided
        refresh_token = request.POST.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (InvalidToken, TokenError):
                return JsonResponse({"error": "Invalid refresh token"}, status=400)

        # Success response
        return JsonResponse({"message": "Successfully logged out"}, status=200)

    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid access token"}, status=401)
    
    
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
            otp_object=OTP.objects.filter(email=email).first()
            otp_object.OTP=otp
            otp_object.save()
            Forgot_otp('chiku',email,otp)
            return JsonResponse({"sucess": "OTP send"}, status=200) if Forgot_otp('chiku',email,otp) else JsonResponse({"error": "Can't send OTP"}, status=401)
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


def create_profile(request):
    jwt_auth = JWTAuthentication()
    try:
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        if request.method=='POST':
            myprofile=Profile.objects.filter(user=request.user).first()
            #get the profile image
            if request.FILES.get('profile_image'):
                profile_image=request.FILES.get('profile_image')
            else:
                profile_image = default_image

            #get the cover image  
            if request.FILES.get('cover_image'):
                cover_image=request.FILES.get('cover_image')
                print(cover_image)
            else:
                cover_image = default_cover_image

            name=request.POST['name']  
            about=request.POST['about']
            school=request.POST['school']
            myprofile.profileimage=profile_image
            myprofile.backgroundimage=cover_image
            #if no name passed used signup time name
            name=name if name else myprofile.name
            myprofile.name=name
            myprofile.about=about
            myprofile.current_study=school
            myprofile.save()
            return JsonResponse({"message":"Success done"},status=201)
        
        #if user wants to edit his profile he will come here
        else:
            myprofile=Profile.objects.filter(user=request.user).first()
            name=myprofile.name
            about=myprofile.about
            school=myprofile.current_study
            context={
                'name':name,
                'about':about,
                'school':school
            }
            return JsonResponse({"userdata":context},200)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)    
        

def view_profile(request,name):
    my_user=request.user
    person_profile=Profile.objects.filter(name=name).first()
    person_obj=person_profile.user
    follower_exist=Followerscount.objects.filter(follower=my_user,user=person_obj).first()
    allfollow=Followerscount.objects.filter(user=person_obj).all()
    allfollow=len(allfollow)
    user_profile=person_profile
    if follower_exist:
        button='UNFOLLOW'
    else:
        button='FOLLOW'    
    person_id=person_profile.user.id
    context={
        'person_id':person_id,
        'myuser':my_user,
        'button':button,
        'number':allfollow,
        'profile':user_profile

    }
    return JsonResponse(context,status=200)



def Follow(request):
    jwt_auth = JWTAuthentication()
    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        user_id=request.GET.get('myuser')
        user=CustomUser.objects.filter(id=user_id).first()
        user_profile=Profile.objects.filter(user=user).first()
        #user_name=user_profile.name
        follower_exist=Followerscount.objects.filter(follower=user,user=user).first()
        if follower_exist:   
            follower_exist.delete()
        else:
            Followerscount.objects.create(follower=user,user=user)
            
        return JsonResponse({"sucess":"Follower updated"}, status=201)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)    

def like_check(request):
    jwt_auth = JWTAuthentication()

    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        like_id=request.GET.get('like_id')
        current_post=Post.objects.filter(id=like_id).first()
        like=Like_post.objects.filter(post_id=like_id,like_user=user).first()
        if like:
            like.delete()
            current_post.no_of_like-=1
        else:
            new_like=Like_post.objects.create(post_id=like_id,like_user=user)
            current_post.no_of_like+=1
        current_post.save()
        data = {
            'likes': current_post.no_of_like
        }
        return JsonResponse(data, status=201)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)

#Add comments    
def Showcomment(request,post_id):
    jwt_auth = JWTAuthentication()

    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        user=request.user
        current_post=Post.objects.filter(id=post_id).first()
        allcomments=Comment.objects.filter(comment_post=current_post)
        recent_user=Profile.objects.filter(user=user).first()
        user=request.user
        context={
        'user':user,
        'allcomments':allcomments,
        'post_id':post_id,
        'recent_user':recent_user
        }
        return JsonResponse(context, status=201)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)

#create comment
def Createcomment(request):
    jwt_auth = JWTAuthentication()

    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        if request.method=="POST":
            comment=request.POST['comment']
            post_id=request.POST['id']
            user=request.user
            user_profile=Profile.objects.filter(user=user).first()
            current_post=Post.objects.filter(id=post_id).first()
            Comment.objects.create(text=comment,comment_by=user_profile,comment_post=current_post)
            current_post.no_of_coment+=1
            user_profile.comment_by_user+=1
            current_post.save()
            user_profile.save()
            return JsonResponse({'success': True}, status=201) 
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)    

    

def Search(request):
    jwt_auth = JWTAuthentication()

    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        if request.method=='POST':
            name=request.POST['searchname']
            users=Profile.objects.filter(name__icontains=name).all()
            return JsonResponse({"profiles":users}, status=201)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)    

   
def Own_profile(request):
    jwt_auth = JWTAuthentication()

    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        user_id=request.GET.get('myuser')
        uy=CustomUser.objects.filter(id=user_id).first()
        user_profile=Profile.objects.filter(user=uy).first()
        my_user=request.user
        #person_profile=Profile.objects.filter(name=n).first()
        person_obj=user_profile.user
        follower_exist=Followerscount.objects.filter(follower=my_user,user=person_obj).first()
        allfollow=Followerscount.objects.filter(user=person_obj).all()
        allfollow=len(allfollow)
        #if recent user is owner of recent pic
        if uy==my_user:
            button='EDIT PROFILE'
        else: 
            #if follow before   
            if follower_exist:
                button='UNFOLLOW'
            #if not follow before   
            else:
                button='FOLLOW'   
            
        person_id=user_profile.user.id
        context={
            'person_id':person_id,
            'myuser':my_user,
            'button':button,
            'number':allfollow,
            'profile':user_profile,
            'user':uy

        }    
        return JsonResponse(context,status=200)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)
#Show your Own profile 
def Own_edit_profile(request):
    jwt_auth = JWTAuthentication()

    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        user_profile=Profile.objects.filter(user=user).first()
        allfollow=Followerscount.objects.filter(user=user)
        allfollow=len(allfollow)
        posts=Post.objects.filter(Q(post_by=user) & Q(postshow=True))
        context={
            'posts':posts,
            'number':allfollow,
            'profile':user_profile,
        }    
        return JsonResponse(context,status=200)
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)
#Delete a picture
def Deletepic(request):
    jwt_auth = JWTAuthentication()
    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        if request.GET.get('value'):
            ownuser=user
            value = request.GET.get('value')
            deletephoto=Post.objects.filter(Q(id=value) & Q(post_by=ownuser)).first()
            deletephoto.postshow=False
            deletephoto.save()
            return JsonResponse({"sucess":"pic delete sucessfully"},status=200)  
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)    

#handle compressed image
def handle_compressed_image(request):
    jwt_auth = JWTAuthentication()

    try:
        # This will check the Authorization header and validate the token
        user, token = jwt_auth.authenticate(request)
        if not user:
            return JsonResponse({"error": "Authentication required"}, status=401)
        if request.method == "POST":
            current_profile=Profile.objects.filter(user=request.user).first()
            text_data = request.POST.get("text_data")
            image_data = request.FILES.get("image_data")
            Post.objects.create(my_post=image_data,post_by=request.user,poster_profile=current_profile,about=text_data)
            return JsonResponse({"message":"Success done"},status=200)    
    except (InvalidToken, TokenError) as e:
        return JsonResponse({"error": "Invalid token"}, status=401)    


