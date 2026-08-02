from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from core_portfolio.forms import *
from core_portfolio.models import *


def portfolio_list(request):
    portfolio_list = Portfolio.objects.all()

    return render(request, 'portfolio/portfolio_list.html', {'portfolio_list': portfolio_list})

def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    return render(request, 'portfolio/portfolio_detail.html', {'portfolio': portfolio})

@login_required
def add_portfolio(request):

    if request.method == "POST":
        form = PortfolioAddForm(request.POST)

        media_formset = PortfolioMediaFormSet(request.POST, request.FILES)

        if form.is_valid() and media_formset.is_valid():
            portfolio = form.save(commit=False)
            portfolio.creator = request.user.profile
            portfolio.save()

            media_formset.instance = portfolio
            media_formset.save()

            return redirect('portfolio-list')
        
    else:
        form = PortfolioAddForm()
        media_formset = PortfolioMediaFormSet()

    return render(request, 'portfolio/add_portfolio.html', {'form': form, 'media_formset': media_formset})

@login_required
def change_portfolio(request, portfolio_id):
    profile = request.user.profile
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    if portfolio.creator != profile:
        return HttpResponseForbidden("Ви не є власником!")
    
    if request.method == "POST":
        form = PortfolioAddForm(
            request.POST,
            instance=portfolio
        )

        media_formset = PortfolioMediaFormSet(
            request.POST,
            request.FILES,
            instance=portfolio
        )
        
        if form.is_valid() and media_formset.is_valid():
            form.save()
            media_formset.save()

            return redirect("portfolio-detail", portfolio_id=portfolio_id)
    
    else:
        form = PortfolioAddForm(instance=portfolio)
        media_formset = PortfolioMediaFormSet(instance=portfolio)

    return render(request, 
                  'portfolio/change_portfolio.html', 
                  {'profile': profile, 
                   'portfolio': portfolio,
                   'media_formset': media_formset,
                   'form': form})

@login_required
def delete_portfolio(request, portfolio_id):
    profile = request.user.profile
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)

    if portfolio.creator != profile:
        return HttpResponseForbidden("Ви не є власником!")
    
    if request.method == "POST":
        portfolio.delete()
        
        return redirect("portfolio-list")
    
    return render(request, 
                  'portfolio/delete_portfolio.html', 
                  {'profile': profile,
                   'portfolio': portfolio})
