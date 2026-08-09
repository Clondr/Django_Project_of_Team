from pathlib import Path 
import json 

BASE_DIR =Path (__file__ ).resolve ().parent .parent 

SECRET_KEY ='django-insecure-=y=85m#y8c*cl=v$4pv0@x#t(+v@4acbq3^#4me=!b^b*_$&w*'

DEBUG =True 

ALLOWED_HOSTS =[]

INSTALLED_APPS =[
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',

'core_profile',
'core_grades',
'core_polls',
'core_events',
'core_portfolio',
'core_gallery',
'core_materials',
'core_forum',
'core_survey',
'core_adverts',
'core_auth_system',
]

MIDDLEWARE =[
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF ='core.urls'

TEMPLATES =[
{
'BACKEND':'django.template.backends.django.DjangoTemplates',
'DIRS':[BASE_DIR /'templates'],
'APP_DIRS':True ,
'OPTIONS':{
'context_processors':[
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
'core_auth_system.context_processors.welcome_banner',
],
},
},
]

WSGI_APPLICATION ='core.wsgi.application'

DATABASES ={
'default':{
'ENGINE':'django.db.backends.sqlite3',
'NAME':BASE_DIR /'db.sqlite3',
}
}

AUTH_PASSWORD_VALIDATORS =[
{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE ='en-us'
TIME_ZONE ='UTC'
USE_I18N =True 
USE_TZ =True 

STATIC_URL ='/static/'
STATICFILES_DIRS =[BASE_DIR /'static']

LOGIN_REDIRECT_URL ='home'
LOGIN_URL ='login'

CSRF_COOKIE_SECURE =True 
CSRF_COOKIE_HTTPONLY =False 
CSRF_COOKIE_SAMESITE ='None'
SESSION_COOKIE_SECURE =True 
SESSION_COOKIE_SAMESITE ='None'

CSRF_TRUSTED_ORIGINS =[
'http://localhost:8000',
'http://127.0.0.1:8000',
'https://apterial-sandra-undevelopmentally.ngrok-free.dev',
'https://*.ngrok-free.dev',
]

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='smtp.gmail.com'
EMAIL_PORT =587 
EMAIL_USE_TLS =True 

with open (Path (BASE_DIR )/'settings.json')as f :
    settings_data =json .load (f )
    EMAIL_HOST_USER =settings_data .get ('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD =settings_data .get ('EMAIL_HOST_PASSWORD')

MEDIA_ROOT =Path (BASE_DIR )/'media'
MEDIA_URL ='/media/'

SECURE_REFERRER_POLICY ='strict-origin-when-cross-origin'
