from typing import Any
from django import forms
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

FORM_UDATE_WIDGET = forms.TextInput(attrs={"class": "form-control mb-1"})


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control mb-1"}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"class": "form-control mb-1"}))
    first_name = forms.CharField(max_length=100, widget=FORM_UDATE_WIDGET)
    last_name = forms.CharField(max_length=100, widget=FORM_UDATE_WIDGET)
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control mb-1"}))
    confirm_password = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control mb-1"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Введенный email уже существует")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_psaword")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return confirm_password

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control mb-1",
            "placeholder": "Введите своё имя"
        }),
    )
    password = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control mb-1",
            "placeholder": "Введите свой пароль"
        }),
    )
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "password", "remember_me")


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=FORM_UDATE_WIDGET)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={"class": "form-control mb-1"}))

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if (email and User.objects.filter(email=email).exclude(
                username=username).exists()):
            raise forms.ValidationError("Email адрес должен быть уникальным")
        return email


class ProfileUpdateForm(forms.ModelForm):

    bio = forms.CharField(max_length=900, widget=FORM_UDATE_WIDGET)
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={"class": "form-control mb-1"}))
    
    class Meta:
        model = Profile
        fields = ("bio", "avatar")
