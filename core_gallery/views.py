from django .shortcuts import render ,redirect ,get_object_or_404 
from core_profile .models import Profile 
from django .http import HttpResponseForbidden 
from django .contrib .auth .decorators import login_required 
from core_gallery .models import *
from core_gallery .forms import *


@login_required 
def gallery_media_list (request ):
    media_list =GalleryMedia .objects .filter (status =GalleryMedia .APPROVED )
    return render (request ,'gallery/gallery_list.html',{'media_list':media_list ,'profile':request .user .profile })

@login_required 
def moderation_gallery (request ):
    profile =request .user .profile 
    if profile .role not in ['moderator','admin']:
        return HttpResponseForbidden ('У вас не має на це прав!')
    media_list =GalleryMedia .objects .filter (status =GalleryMedia .ON_CHECKING )
    return render (request ,'gallery/moderation_gallery.html',{'media_list':media_list })

@login_required 
def upload_to_gallery (request ,profile_id ):
    profile =get_object_or_404 (Profile ,pk =profile_id )
    if request .method =='POST':
        form =GalleryMediaUploadForm (request .POST ,request .FILES )
        if form .is_valid ():
            GalleryMedia .objects .create (
            profile_id =profile ,
            media =form .cleaned_data ['media'],
            uploaded_by =request .user .profile 
            )
            return redirect ('gallery-list')
    else :
        form =GalleryMediaUploadForm ()
    return render (request ,'gallery/add_media.html',{'form':form ,'profile':profile })

@login_required 
def approve_addition (request ,media_id ):
    if request .method !="POST":
        return HttpResponseForbidden ()
    profile =request .user .profile 
    if profile .role not in ['moderator','admin']:
        return HttpResponseForbidden ("У вас не має на це прав!")
    media =get_object_or_404 (GalleryMedia ,id =media_id )
    media .status =GalleryMedia .APPROVED 
    media .save ()
    return redirect ('gallery-list')
