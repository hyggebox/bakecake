from django.shortcuts import render

from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm


class SignUp(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('render_lk_page')
    template_name = 'registration/register.html'