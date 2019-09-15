from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.signup, name='signup'),
    path('sign/<docid>', views.sign, name='sign'),
    path('', views.index, name='index'),
]
