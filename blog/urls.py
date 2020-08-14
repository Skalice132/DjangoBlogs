"""BlogDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowPostView.as_view(), name='blog-home'),
    path('progress/', views.progress, name='progress'),
    path('feedback/', views.feedback, name='feedback'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('user/<str:username>/', views.UserAllPostView.as_view(), name='user-news'),
    path('tags/<str:name>/', views.TagAllPostView.as_view(), name='tag-news'),
    path('news/<int:pk>/', views.DetailPostView.as_view(), name='news-detail'),
    path('news/add/', views.CreatePostView.as_view(), name='news-add'),
    path('news/<int:pk>/update/', views.UpdatePostView.as_view(), name='news-update'),
    path('news/<int:pk>/delete/', views.DeletePostView.as_view(), name='news-delete'),
]
