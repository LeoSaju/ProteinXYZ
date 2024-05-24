from django.urls import path
from . import views

urlpatterns = [
    path('protein/', views.protein_view, name='protein_view'),
]