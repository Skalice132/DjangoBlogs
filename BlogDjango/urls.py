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
from django.contrib.auth import views as authViews
from django.contrib import admin
from django.urls import path, include
from users import views as userViews
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('blog.urls')),
    path('reg/', userViews.register, name='reg'),
    path('profile/', userViews.profile, name='profile'),
    path('login/', authViews.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('pass-reset/', authViews.PasswordResetView.as_view(template_name='users/pass_reset.html'), name='pass-reset'),
    path('password_reset_confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='users/pass_reset_confirm.html'), name='password_reset_confirm'),
    path('pass-reset/done/', authViews.PasswordResetDoneView.as_view(template_name='users/pass_reset_done.html'), name='pass_reset_done'),
    path('pass-reset/complete/', authViews.PasswordResetCompleteView.as_view(template_name='users/pass_reset_complete.html'), name='pass_reset_complete'),
    path('logout/', authViews.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
