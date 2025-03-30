from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model

from users.forms import UserCreationForm


User = get_user_model()


class SignupPageView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"
