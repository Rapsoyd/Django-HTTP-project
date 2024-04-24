from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserUpdateForm, ProfileUpdateForm, LoginForm
from django.views import generic
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    initial = None
    template_name = "blog/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Передаем в form экземпляр класса с установленным словарем initial
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to="/")

        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'blog/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ваш профиль успешно обновлен")
            redirect(to='user-profile')

    else:
        user_form = UserUpdateForm()
        user_form.instance = request.user
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "blog/profile.html", {
        'user_form': user_form,
        "profile_form": profile_form
    })
