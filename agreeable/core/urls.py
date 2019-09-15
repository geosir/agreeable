from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.signup, name='signup'),
    path('finish/', views.addkey, name='finish'),
    path('done/', views.done, name='done'),
    path('validate_preview/', views.validatePreview, name='validate_preview'),
    path('validate/', views.validate, name='validate'),
    path('sign/<docid>', views.sign, name='sign'),
    path('asksign/<docid>', views.asksign, name='asksign'),
    path('fail/', views.fail, name='fail'),
    path('sign_yes/<docid>', views.sign_yes, name='sign_yes'),
    path('sign_no/', views.sign_no, name='sign_no'),
    path('fail/', views.fail, name='fail'),
    path('', views.index, name='index'),
]
