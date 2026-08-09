from django .shortcuts import render ,redirect 
from django .views .decorators .http import require_POST 
from django .views .decorators .csrf import csrf_protect 
from django .core .mail import EmailMultiAlternatives 
from django .template .loader import render_to_string 
from django .utils .http import urlsafe_base64_encode ,urlsafe_base64_decode 
from core_auth_system .tokens import account_activation_token 
from django .utils .encoding import force_bytes ,force_str 
from django .urls import reverse 
from django .contrib .auth import authenticate ,login ,logout 
from django .contrib .auth .forms import AuthenticationForm 
from django .contrib .auth .models import User 
from django .contrib import messages 
from core_auth_system .forms import *
from django .contrib .auth .decorators import login_required 


@csrf_protect 
@require_POST 
def accept_offer (request ):
    response =redirect ('home')
    response .set_cookie (
    'site_offer_accepted',
    'true',
    max_age =60 *60 *24 *30 ,
    httponly =False ,
    samesite ='Lax',
    )
    request .session ['banner_shown']=True 
    return response 


def register (request ):
    if request .method =='POST':
        form =RegisterUserForm (request .POST )
        if form .is_valid ():
            user =form .save (commit =False )
            email =form .cleaned_data .get ('email')
            user .is_active =True 
            user .save ()
            login (request ,user )
            if email :
                token =account_activation_token .make_token (user )
                uid =urlsafe_base64_encode (force_bytes (user .pk ))
                activation_link =request .build_absolute_uri (
                reverse ('activate-account',kwargs ={'uidb64':uid ,'token':token })
                )
                context ={
                'username':user .username ,
                'activation_link':activation_link ,
                }
                subject ='Активація вашого облікового запису'
                email_message =EmailMultiAlternatives (
                subject =subject ,
                body =f'Активуйте аккаунт по посиланню: {activation_link }',
                from_email ='bkirilleb09@gmail.com',
                to =[user .email ]
                )
                html_content =render_to_string ('auth_system/activation_email.html',context )
                email_message .attach_alternative (html_content ,"text/html")
                try :
                    email_message .send ()
                except Exception :
                    pass 
            return redirect ('profile')
    else :
        form =RegisterUserForm ()
    return render (request ,'auth_system/register.html',context ={'form':form })


def activate_account (request ,uidb64 ,token ):
    try :
        uid =force_str (urlsafe_base64_decode (uidb64 ))
        user =User .objects .get (pk =uid )
    except (TypeError ,ValueError ,OverflowError ,User .DoesNotExist ):
        user =None 

    if user is not None and user .email and account_activation_token .check_token (user ,token ):
        user .is_active =True 
        user .save ()
        return redirect ('profile')
    return redirect ('home')


def login_view (request ):
    if request .method =="POST":
        form =AuthenticationForm (request ,data =request .POST )
        if form .is_valid ():
            user =form .get_user ()
            login (request ,user )
            return redirect ('profile')
    else :
        form =AuthenticationForm (request )

    for field in form .fields .values ():
        field .widget .attrs ['class']='form-control'

    return render (request ,'auth_system/login.html',{"form":form })


@login_required 
def logout_view (request ):
    logout (request )
    return redirect ('login')


def home (request ):
    return render (request ,'home.html')
