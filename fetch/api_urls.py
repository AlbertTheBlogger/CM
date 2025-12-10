from django.urls import path
from . import views

urlpatterns = [
    path('hot-keywords/', views.get_hot_keywords, name='get_hot_keywords'),
    path('results/', views.fetch_results_api, name='fetch_results_api'),
]