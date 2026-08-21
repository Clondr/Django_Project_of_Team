from django .shortcuts import render ,get_object_or_404 ,redirect 
from django .contrib .auth .decorators import login_required 
from .models import Profile 
from django .db .models import Avg 
from .forms import *

@login_required 
def change_profile (request ):
    profile =get_object_or_404 (Profile ,user =request .user )
    profile .auto_give_role ()

    if request .method =='POST':
        form =UploadAvatarForm (request .POST ,request .FILES )
        if form .is_valid ():
            profile .bio =request .POST .get ('bio',profile .bio )
            if 'avatar'in request .FILES and request .FILES ['avatar']:
                profile .avatar =request .FILES ['avatar']
            profile .save ()
            return redirect ('profile')
    else :
        form =UploadAvatarForm ()

    return render (request ,'profile/edit_profile.html',{'form':form ,'profile':profile })

@login_required 
def change_detail_profile (request ,pk ):
    profile =get_object_or_404 (Profile ,user =request .user ,pk =pk )
    profile .auto_give_role ()

    if request .method =='POST':
        form =UploadAvatarForm (request .POST ,request .FILES )
        if form .is_valid ():
            profile .bio =request .POST .get ('bio',profile .bio )
            if 'avatar'in request .FILES and request .FILES ['avatar']:
                profile .avatar =request .FILES ['avatar']
            profile .save ()
            return redirect ('profile-detail',pk =pk )
    else :
        form =UploadAvatarForm ()

    return render (request ,'profile/edit_detail_profile.html',{'form':form ,'profile':profile })

def profile_detail (request ,pk ):
    profile =get_object_or_404 (Profile ,pk =pk )
    average_score =profile .grades .aggregate (avg_score =Avg ('score'))['avg_score']
    profile .auto_give_role ()
    return render (request ,'profile/profile_detail.html',{'profile':profile ,'average_score':average_score })

@login_required 
def profile (request ):
    profile =get_object_or_404 (Profile ,user =request .user )
    average_score =profile .grades .aggregate (avg_score =Avg ('score'))['avg_score']
    profile .auto_give_role ()
    return render (request ,'profile/profile.html',{'profile':profile ,'average_score':average_score })
