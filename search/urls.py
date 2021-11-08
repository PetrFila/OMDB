from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchView.as_view(), name='search-form'),
    path('result/', views.ResultView.as_view(), name='found-titles'),
    path('result/<int:pk>/', views.DetailView.as_view(), name='title-detail'),

    # path('', views.search_form, name='search-form'),
    # path('result/', views.find_title, name='found-titles'),
    # path('result/<int:pk>/', views.title_detail, name='title-detail'),

]
