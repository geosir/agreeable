from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.signup, name='signup'),
    path('finish/', views.addkey, name='finish'),
    path('done/', views.done, name='done'),
    path('validate_preview/', views.validatePreview, name='validate_preview'),
    path('sign/<docid>', views.sign, name='sign'),
    path('', views.index, name='index'),
]
