from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone
from .forms import UserOurRegistration, ProfileImage, UserUpdateForm


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
        'date': timezone.now,
        'form': form,
        'title': 'Регистрация пользователя'})

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
        'date': timezone.now,
        'img_profile': img_profile,
        'update_user': update_user,
        'title': 'Профиль'})
