from django.urls import path
from . import views

urlpatterns = [
    path('select/', views.analyse_select_api, name='analyse_select_api'),
    path('results/', views.analyse_results_api, name='analyse_results_api'),
    path('pending/', views.get_pending_comments, name='get_pending_comments'),
]