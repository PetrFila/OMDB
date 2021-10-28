from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_form, name='search-form'),
    path('result/', views.find_title, name='found-titles'),
    path('result/<int:pk>/', views.title_detail, name='title-detail'),

]
