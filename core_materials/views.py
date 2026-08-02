from django.shortcuts import render, redirect, get_object_or_404
from core_materials.models import *
from core_profile.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from core_materials.forms import *


def materials_list(request):
    materials_list = Materials.objects.all()

    return render(request, 'materials/materials_list.html', {'materials_list': materials_list})

def material_detail(request, material_id):
    material = get_object_or_404(Materials, pk=material_id)

    return render(request, 'materials/material_detail.html', {'material': material})

@login_required
def add_material(request):
    profile= request.user.profile

    if profile.role not in ['moderator', 'admin']:
        return HttpResponseForbidden("У вас не має на це прав!")

    if request.method == "POST":
        form = AddMaterialForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('materials-list')
        
    else:
        form = AddMaterialForm()

    return render(request, 'materials/add_material.html', {'form': form})
    
@login_required
def change_material(request, material_id):
    profile= request.user.profile
    material = get_object_or_404(Materials, pk=material_id)

    if profile.role not in ['moderator', 'admin']:
        return HttpResponseForbidden("У вас не має на це прав!")


    if request.method == 'POST':
        form = AddMaterialForm(
            request.POST,
            request.FILES,
            instance=material
        )

        if form.is_valid():
            form.save()

            return redirect('material-detail', material_id=material.id)
        
    else:
        form = AddMaterialForm(instance=material)

    return render(request, 
                    'materials/change_material.html',
                    {'form': form, 
                    'material': material, 
                    'profile': profile})
    
@login_required
def delete_material(request, material_id):
    profile= request.user.profile
    material = get_object_or_404(Materials, pk=material_id)

    if profile.role not in ['moderator', 'admin']:
        return HttpResponseForbidden("У вас не має на це прав!")
    
    if request.method == "POST":
        material.delete()

        return redirect("materials-list")

    return render(request, 'materials/delete_material.html', {'material': material, 'profile': profile})



