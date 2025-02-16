from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
                                      PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, hashers
from django.urls import reverse_lazy
from config import settings
from .models import Profile
from .forms import UserCreationForm
from django.contrib import messages
from .models import User
from django.contrib.auth.forms import PasswordResetForm

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/account/login/'
    template_name = 'pages/signup.html'

    def form_valid(self, form):
        messages.success(self.request, 'Sucessed user creation')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid signup information')
        return super().form_invalid(form)
    
class Login(LoginView):
    template_name = 'pages/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Login successed')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login information')
        return super().form_invalid(form)
    
class Logout(LogoutView):
    template_name = 'pages/login.html'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ('username', 'email')
    success_url = '/account/'

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('current_password'):
            user = User.objects.get(pk=request.user.pk)
            valid = True
            if not user.check_password(request.POST.get('current_password')):
                valid = False
                messages.error(request, 'Current password is wrong')

            if request.POST.get('password') != request.POST.get('password_confirm'):
                valid = False
                messages.error(request, 'Mismatch new passwords')

            if valid:
                user.password = hashers.make_password(request.POST.get('password'))
                user.save()
            
        return super().post(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        messages.success(self.request, 'Updated')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Error')
        return super().form_invalid(form)
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    fields = ('name', 'zipcode', 'prefecture',
              'city', 'address1', 'address2', 'tel')
    success_url = '/profile/'

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()
    
    def form_valid(self, form):
        messages.success(self.request, 'Updated')
        return super().form_valid(form)
    

class PasswordReset(PasswordResetView):
    email_template_name = "pages/registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = settings.TITLE
    html_email_template_name = None
    subject_template_name = "pages/registration/password_reset_subject.txt"
    success_url = reverse_lazy('password_reset_done')
    template_name = "pages/registration/password_reset_form.html"
    #title = _("Password reset")
    #token_generator = default_token_generator

    def form_valid(self, form):
        return super().form_valid(form)

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'pages/registration/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'pages/registration/password_reset_confirm.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Password reset successed')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error')
        return super().form_invalid(form)
    
class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'pages/registration/password_reset_complete.html'