from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('subscribeme', views.subscribeme, name='subscribeme'),

    path('category/<int:id>/', views.index, name='index'),

    path('submitcontact', views.submitcontact, name='submitcontact'),

]