from django.urls import path
from core_portfolio.views import portfolio_list, portfolio_detail, change_portfolio, add_portfolio, delete_portfolio

urlpatterns = [
    path('portfolio-list/', portfolio_list, name='portfolio-list'),
    path('portfolio-detail/<int:portfolio_id>/', portfolio_detail, name='portfolio-detail'),
    path('change-portfolio/<int:portfolio_id>/', change_portfolio, name='change-portfolio'),
    path('add-portfolio/', add_portfolio, name='add-portfolio'),
    path('delete-portfolio/<int:portfolio_id>/', delete_portfolio, name='delete-portfolio'),
]
