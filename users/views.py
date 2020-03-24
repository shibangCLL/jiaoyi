from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from .forms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .tool import RenderWrite


# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            email = form.clean_email()
            password1 = form.clean_password1()
            password2 = form.clean_password2()

            user = User.objects.create_user(username=username, password=password2, email=email)
            UserProfile.objects.create(user=user)
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = RegistrationForm()
        title = "注册"
    return RenderWrite.render_template(request, 'jiaoyi/registration.html', {'form': form, 'title': title})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.cleaned_data['password']
            try:
                user = auth.authenticate(username=username, password=password)
                print('111')
            except Exception as e:
                print(e)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'))
            else:
                return render(request, 'jiaoyi/login.html', {'form': form, 'message': '密码错误'})

    form = LoginForm()
    title = "登陆"
    return RenderWrite.render_template(request, 'jiaoyi/login.html', {'form': form, 'title': title})


@login_required(login_url='/users/login')
def profile(request):
    # user = get_object_or_404(User, pk=pk)
    # return render(request, 'jiaoyi/account.html', locals())
    user = request.user
    # user_profile = get_object_or_404(UserProfile, user=user)
    # if request.method == "POST":
    #     form = ProfileForm(request.POST)
    #     if form.is_valid():
    #         user.first_name = form.cleaned_data['first_name']
    #         user.last_name = form.cleaned_data['last_name']
    #         # user.email = form.clean_email()
    #         user.save()
    #         user_profile.org = form.cleaned_data['org']
    #         user_profile.telephone = form.cleaned_data['telephone']
    #         user_profile.save()
    #         return HttpResponseRedirect(reverse('users:profile'))
    # else:
    #     default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
    #                     'org': user.profile.org, 'telephone': user.profile.telephone, }
    #     form = ProfileForm(default_data)
    form = ProfileForm()
    title = "个人信息"
    return RenderWrite.render_template(request, 'jiaoyi/account.html', {'form': form, 'user': user, 'title': title})


@login_required(login_url='/users/login')
def changeprofile(request):
    # user = get_object_or_404(User, pk=pk)
    # return render(request, 'jiaoyi/account.html', locals())
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            # user.email = form.clean_email()
            user.save()
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                        'org': user.profile.org, 'telephone': user.profile.telephone, }
        form = ProfileForm(default_data)
        title="修改信息"
    return RenderWrite.render_template(request, 'jiaoyi/accout-detail.html', {'form': form, 'user': user, 'title': title})


@login_required(login_url='/users/login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/users/login/")
