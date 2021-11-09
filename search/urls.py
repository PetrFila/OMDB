from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchView.as_view(), name='search-form'),
    path('result/', views.ResultView.as_view(), name='found-titles'),
    path('result/<int:pk>/', views.DetailTitleView.as_view(), name='title-detail'),
]
