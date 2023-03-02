from django.urls import path, include
from . import views


app_name = 'accounts'
reset_password_url = [
	path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns = [
	path('', include(reset_password_url)),
	path('register/', views.UserRegisterView.as_view(), name='user_register'),
	path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
	path('login/', views.UserLoginView.as_view(), name='user_login'),
	path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
	path('profile/', views.UserAccountsView.as_view(), name='user_profile'),
    
]