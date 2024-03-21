from django.contrib.auth import views
from django.urls import path, reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .views import UserDeleteView, UserUpdateView

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path('profile/<username>/', UserUpdateView.as_view(), name='profile'),
    path('delete/<username>', UserDeleteView.as_view(), name='delete'),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html'
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name="password_change_done",
    ),
    path(
        'password_reset/',
        views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html'
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path(
        'registration/',
        CreateView.as_view(
            template_name='users/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),
]
