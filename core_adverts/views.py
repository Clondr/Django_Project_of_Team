from django .shortcuts import render ,redirect ,get_object_or_404 
from django .http import HttpResponseForbidden 
from django .contrib .auth .decorators import login_required 
from core_adverts .models import *
from core_adverts .forms import *
from core_profile .models import Profile 


def advert_list (request ):
    adverts_list =Advertisement .objects .all ()

    return render (request ,'adverts/adverts_list.html',{'adverts_list':adverts_list })

def advert_detail (request ,pk ):
    advert =get_object_or_404 (Advertisement ,pk =pk )

    return render (request ,'adverts/advert_detail.html',{'advert':advert })

@login_required 
def add_advert (request ):
    profile =request .user .profile 

    if profile .role =='moderator'or profile .role =='admin':
        if request .method =='POST':
            form =CreateAdvertForm (request .POST ,request .FILES )
            if form .is_valid ():
                advert =Advertisement .objects .create (
                advert_title =form .cleaned_data ['advert_title'],
                content =form .cleaned_data ['content'],
                content_image =form .cleaned_data ['content_image'],
                creator =request .user .profile ,
                )


                return redirect ('adverts-list')
        else :
            form =CreateAdvertForm ()

        return render (request ,'adverts/advert_creation_form.html',{'form':form })

    return HttpResponseForbidden ("Ви не маєте на це прав!")

@login_required 
def update_advert (request ,pk ):
    advert =get_object_or_404 (Advertisement ,pk =pk )


    profile =request .user .profile 

    if profile .role not in ('moderator','admin'):
        return HttpResponseForbidden ('У вас немає на це прав!')

    else :
        if request .method =="POST":
            form =CreateAdvertForm (
            request .POST ,
            request .FILES ,
            instance =advert 
            )

            if form .is_valid ():
                form .save ()

                return redirect ('advert-detail',pk =advert .pk )
        else :
            form =CreateAdvertForm (instance =advert )

    return render (request ,'adverts/update_advert_form.html',{'form':form ,'advert':advert })

@login_required 
def delete_advert (request ,pk ):
    advert =get_object_or_404 (Advertisement ,pk =pk )

    profile =request .user .profile 

    if profile .role not in ('moderator','admin'):
        return HttpResponseForbidden ('У вас немає на це прав!')

    if request .method =='POST':
        advert .delete ()

        return redirect ('adverts-list')

    return render (request ,'adverts/delete_advert.html',{'advert':advert })