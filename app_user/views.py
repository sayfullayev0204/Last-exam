from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .forms import UserCreationForm

User = get_user_model()


class UserRegistration(CreateView):
    model = User
    template_name = 'app_user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        response = super().form_valid(form)
        user = self.object
        # Email yuborish
        send_mail(
            subject='Thank you for registering',
            message=f'DEAR {user.username},  You have successfully registered.',
            from_email='odiloffr"gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return response


def user_logout(request):
    logout(request)
    return redirect('home')


class Account(UpdateView):
    model = User
    template_name = 'app_user/account.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(User, pk=user_id)
