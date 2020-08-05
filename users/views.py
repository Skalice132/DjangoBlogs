from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone
from .forms import UserOurRegistration, ProfileImage, UserUpdateForm
from django.contrib.auth.models import User
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def profiles(request):
    user = request.GET.get('user')
    if user:
        search = User.objects.all().filter(username__contains=user)
    else:
        search = User.objects.all()

    return render(request,
                  'users/profiles.html',
                  {'title': 'Список пользователей',
                   'users_list': search
                   })

class ProfileDetailView(View):
    def get(self,request, pk):
        profiles = User.objects.get(id=pk)
        return render(request,
                  'users/profile.html',
                  {'title': 'Пользователь',
                   'object_list': profiles
                   })


def register(request):
    if request.method == 'POST':
        form = UserOurRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользовтель {username} добавлен в черный список')
            return redirect('blog-home')
    else:
        form = UserOurRegistration()

    return render(request, 'users/registration.html', {
        'title': 'Регистрация пользователя',
        'date': timezone.now,
        'form': form
        })

@login_required
def profile(request):
    if request.method == 'POST':
        img_profile = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
        update_user = UserUpdateForm(request.POST, instance=request.user)

        if update_user.is_valid() and img_profile.is_valid():
            update_user.save()
            img_profile.save()
            messages.success(request, f'Данные были изменены')
            return redirect('profile')
    else:
        img_profile = ProfileImage(instance=request.user.profile)
        update_user = UserUpdateForm(instance=request.user)

    return render(request,'users/profile.html', {
        'title': 'Профиль',
        'date': timezone.now,
        'img_profile': img_profile,
        'update_user': update_user
        })
