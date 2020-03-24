from django import forms
from django.contrib.auth.models import User
import re


def email_check(email):
    pattern = re.compile('^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$')
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50,
                               widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))
    email = forms.EmailField(label='邮箱', widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={'class': "form-control", 'type': 'text'}))
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={'class': "form-control", 'type': 'text'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 2:
            raise forms.ValidationError('用户名太短，至少要两个字符')
        elif len(username) > 50:
            raise forms.ValidationError('用户名太长，不能超过50个字符')
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError('用户名已经存在')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # filter_result = User.objects.filter(email__exact=email)
        # if len(filter_result) > 0:
        #     raise forms.ValidationError('邮箱已经存在')
        #
        # return email

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError('邮箱已经存在')
        else:
            raise forms.ValidationError('请输入一个有效邮箱')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码太短，至少为6个字符")
        elif len(password1) > 20:
            raise forms.ValidationError("密码太长，不能超过20个字符")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入的密码不一样，请重新输入.")

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50,
                               widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': "form-control", 'type': 'text'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("该邮箱不存在")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("用户名不存在，请先注册")
        return username


class ProfileForm(forms.Form):
    first_name = forms.CharField(label='名字', max_length=50, required=False,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))
    last_name = forms.CharField(label='姓氏', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))
    org = forms.CharField(label='部门', max_length=50, required=False,
                          widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))
    telephone = forms.CharField(label='手机号', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))
    # email = forms.EmailField(label='邮箱',widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text'}))

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     # filter_result = User.objects.filter(email__exact=email)
    #     # if len(filter_result) > 0:
    #     #     raise forms.ValidationError('邮箱已经存在')
    #     #
    #     # return email
    #
    #     if email_check(email):
    #         filter_result = User.objects.filter(email__exact=email)
    #         if len(filter_result) > 0:
    #             raise forms.ValidationError('邮箱已经存在')
    #     else:
    #         raise forms.ValidationError('请输入一个有效邮箱')
    #     return email


class PwdChangeForm(forms.Form):
    pass
