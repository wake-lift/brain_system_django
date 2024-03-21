from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import DeleteView, UpdateView

from .forms import UserUpdateForm

User = get_user_model()


class UserUpdateView(UpdateView):
    slug_url_kwarg = 'username'
    slug_field = 'username'
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.kwargs['username']})


class UserDeleteView(DeleteView):
    slug_url_kwarg = 'username'
    slug_field = 'username'
    model = User
    template_name = 'users/delete_user.html'

    def get_success_url(self):
        return reverse('common_pages:main')
