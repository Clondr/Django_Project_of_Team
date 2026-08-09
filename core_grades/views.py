from django .shortcuts import render ,get_object_or_404 ,redirect 
from .models import Grade 
from core_profile .models import Profile 
from .forms import AddGradeForm 
from django .contrib .auth .decorators import login_required 

@login_required 
def add_grade (request ,pk ):
    profile =get_object_or_404 (Profile ,pk =pk )
    if request .method =='POST':
        form =AddGradeForm (request .POST )
        if form .is_valid ():
            if profile .role in ['admin','moderator']:
                form .add_error (None ,'Неможливо додати оцінку адміну або модератору.')
            else :
                grade =form .save (commit =False )
                grade .profile =profile 
                grade .save ()
                return redirect ('profile-detail',pk =pk )
    else :
        form =AddGradeForm ()

    return render (request ,'grades/grade_creation_form.html',{'form':form ,'profile':profile })

@login_required 
def list_grades (request ,pk ):
    profile =get_object_or_404 (Profile ,pk =pk )
    grades =profile .grades .all ()
    return render (request ,'grades/grades_list.html',{'grades':grades ,'profile':profile })

@login_required 
def edit_grade (request ,pk ):
    grade =get_object_or_404 (Grade ,pk =pk )

    if request .method =='POST':
        form =AddGradeForm (request .POST ,instance =grade )
        if form .is_valid ():
            form .save ()
            return redirect ('list-grades',pk =grade .profile .pk )
    else :
        form =AddGradeForm (instance =grade )

    return render (request ,'grades/grades_edit.html',{'form':form ,'grade':grade })

@login_required 
def delete_grade (request ,pk ):
    grade =get_object_or_404 (Grade ,pk =pk )

    if request .method =='POST':
        grade .delete ()
        return redirect ('list-grades',pk =grade .profile .pk )

    return render (request ,'grades/grades_delete_confirm.html',{'grade':grade })

@login_required 
def search_user_for_moderator (request ):
    if request .user .profile .role not in ['admin','moderator']:
        return redirect ('home')
    query =request .GET .get ('q')
    if query :
        profiles =Profile .objects .filter (role ='user',user__username__icontains =query )
    else :
        profiles =Profile .objects .filter (role ='user')
    return render (request ,'grades/search_user.html',{'users':profiles ,'query':query })
