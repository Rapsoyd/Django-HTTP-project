from django.urls import path
from accounts.views import SignUpView, CustomLoginView, profile
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name='signup'),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(template_name="blog/logout.html"), name='logout'),
    path('profile/', profile, name='user-profile')
]