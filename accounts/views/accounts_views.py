from urllib.parse import urlparse, urlunparse
from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_not_required, login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from django.views.generic.edit import FormView,CreateView
from accounts.forms.form import CustomUserCreationForm
from django.contrib.auth.models import Permission
from django.contrib import messages




class RedirectURLMixin:
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url_allowed_hosts = set()

    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name)
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        raise ImproperlyConfigured("No URL to redirect to. Provide a next_page.")


@method_decorator(login_not_required, name="dispatch")
class LoginView(RedirectURLMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    redirect_authenticated_user = True

class LogoutView(RedirectURLMixin, TemplateView):
    """
    Log out the user and display the 'You are logged out' message.
    """
    pass


class RegisterView(CreateView):
    form_class  = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        user.user_permissions.add(Permission.objects.get(codename='view_login'))
        messages.success(self.request, 'Your account has been created! You can now log in.')

        return response
    
    def form_invalid(self, form):
        # Display an error message to the user when registration fails
        messages.error(self.request, 'There was an error with your registration. Please try again.')
        # Call the parent class's form_invalid method to handle the invalid form submission
        return super().form_invalid(form)