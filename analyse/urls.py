from django.urls import path
from . import views

app_name = 'analyse'
urlpatterns = [
    path('select/', views.analyse_select, name='select'),
    path('results/', views.analyse_results, name='results'),
]