from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_form, name='search-form'),
    path('result/', views.find_title, name='found-titles'),
    # path('post/new/', views.post_new, name='post_new'),
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]
