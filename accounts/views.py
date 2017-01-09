from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

import os

from . import models
from . import forms


def handle_file_upload(file, file_destination):
    file_destination = os.path.join("assets", file_destination)
    with open(file_destination, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def sign_up(request):
    if request.method == 'POST':
        form = forms.SignUpForm(data=request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            new_user = User(
                username=form_data['username'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
            )
            new_user.set_password(form_data['password'])
            new_user.save()
            new_profile = models.UserProfile(user=new_user)
            new_profile.save()
            user = authenticate(
                username=form_data['username'],
                password=form_data['password']
            )
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                message="You are signed up, logged in, and can "
                        "complete your profile",
            )
            return redirect('accounts:edit_profile', pk=user.pk)
    else:
        form = forms.SignUpForm()
    return render(request, 'accounts\sign_up.html', {'form': form})


def sign_in(request):
    form = forms.UserAuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(user.profile.get_absolute_url())
            else:
                messages.add_message(request,
                                     level=messages.ERROR,
                                     message="Account Inactive")
        else:
            messages.add_message(
                request,
                level=messages.ERROR,
                message="Invalid details, or user does not exist"
            )
    return render(request, 'accounts\sign_in.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.add_message(request, level=messages.SUCCESS, message="Logged out successfully")
    return redirect('home')


@login_required
def show_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    privileged = False
    if user == request.user:
        privileged = True
    profile = get_object_or_404(models.UserProfile, user=user)
    context = {
        'profile': profile,
        'privileged': privileged,
    }
    template = 'accounts\profile.html'
    return render(request, template, context)


@login_required
def edit_profile(request, pk):
    profile_to_edit = get_object_or_404(
        models.UserProfile,
        user=request.user
    )
    form = forms.EditProfileForm(instance=profile_to_edit)
    if request.method == 'POST':
        form = forms.EditProfileForm(
            request.POST or None,
            request.FILES,
            instance=profile_to_edit,
        )
        if form.is_valid():
            profile_to_edit = form.save(commit=False)
            profile_to_edit.avatar = profile_to_edit.generate_file_path()
            if request.FILES:
                handle_file_upload(
                    request.FILES['avatar'],
                    profile_to_edit.avatar
                )
            profile_to_edit.save()
            messages.success(request, message="Your profile is updated")
            return HttpResponseRedirect(profile_to_edit.get_absolute_url())
    return render(request, 'accounts\edit_profile.html', {'form': form})


@login_required
def edit_image():
    pass


@login_required
def change_user_password(request):
    form = forms.ChangePasswordForm()
    if request.method == 'POST':
        form = forms.ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            u = form.user
            u.set_password(request.POST['new_password'])
            u.save()
            update_session_auth_hash(request, u)
            messages.success(
                request,
                message="Your password has been changed"
            )
            HttpResponseRedirect(u.profile.get_absolute_url())
    return render(request, 'accounts\change_password.html', {'form': form})
