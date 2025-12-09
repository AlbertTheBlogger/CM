from django.urls import path
from . import views

app_name = 'fetch'
urlpatterns = [
    path('', views.fetch_main, name='main'),
    path('results/', views.fetch_results, name='results'),
]