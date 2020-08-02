from django.urls import path
from django.contrib.auth import views as authViews
from users import views as userViews
from . import views

urlpatterns = [
    #path('profile/', userViews.profile, name='profile'),
    path('profile/', userViews.profile, name='profile'),
    path('profiles/', userViews.profiles, name='profiles'),
    path('reg/', userViews.register, name='reg'),
    path('login/', authViews.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('pass-reset/', authViews.PasswordResetView.as_view(template_name='users/pass_reset.html'), name='pass-reset'),
    path('password_reset_confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='users/pass_reset_confirm.html'), name='password_reset_confirm'),
    path('pass-reset/done/', authViews.PasswordResetDoneView.as_view(template_name='users/pass_reset_done.html'), name='pass_reset_done'),
    path('pass-reset/complete/', authViews.PasswordResetCompleteView.as_view(template_name='users/pass_reset_complete.html'), name='pass_reset_complete'),
    path('logout/', authViews.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
