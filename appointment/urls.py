from django.urls import path
from . import views

urlpatterns = [
    path('add_custom/', views.custom_add_appointment, name='add_custom_appointment'),
]
