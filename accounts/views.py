from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

import random
from utils import send_otp_code
from .models import OtpCode, User
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm

class UserRegisterView(View):
	form_class = UserRegistrationForm
	template_name = 'accounts/register.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			random_code = random.randint(1000, 9999)
			send_otp_code(cd['phone'], random_code)
			OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
			# --------------- Session ---------------  
			request.session['user_registration_info'] = {
				'phone_number': cd['phone'],
				'email': cd['email'],
				'full_name': cd['full_name'],
				'password': cd['password'],
			}
			messages.success(request, 'we sent you a code', 'success')
			return redirect('accounts:verify_code')
		return render(request, self.template_name, {'form':form})

class UserRegisterVerifyCodeView(View):
	template_name = 'accounts/verify.html'
	form_class = VerifyCodeForm

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		user_session = request.session['user_registration_info']
		code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if cd['code'] == code_instance.code:
				User.objects.create_user(user_session['phone_number'], user_session['email'],
										 user_session['full_name'], user_session['password'])

				code_instance.delete()
				messages.success(request, 'you registered.', 'success')
				return redirect('home:home')
			else:
				messages.error(request, 'this code is wrong', 'danger')
				return redirect('accounts:verify_code')
		return redirect('home:home')


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'accounts/login.html'

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, 
								phone_number=cd['phone'], 
								password=cd['password'])

			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'info')
				return redirect('products:products')

			messages.error(request, 'phone or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})

class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'you logged out successfully', 'success')
		return redirect('products:products')


# -------------------- Reset Password---------------------------
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

# -------------------- End Reset Password---------------------------


class UserAccountsView(LoginRequiredMixin, View):
	template_name = 'accounts/profile.html'
	
	def get(self, request):
		user = request.user
		user_orders = user.orders.all()

		context = {
			'profile': user,
			'orders': user_orders
		}
		return render(request, self.template_name, context)
	