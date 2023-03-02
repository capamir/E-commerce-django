from django.urls import path, include
from . import views


app_name = 'accounts'
reset_password_urls = [
	path('', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

authorization_urls = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
	path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
	path('login/', views.UserLoginView.as_view(), name='user_login'),
	path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
]

profile_urls = [
	path('', views.UserAccountView.as_view(), name='user_profile'),
	path('edit/', views.UserAccountEditView.as_view(), name='user_edit_profile'),
    
]
    
urlpatterns = [
	path('', include(authorization_urls)),
	path('reset/', include(reset_password_urls)),
	path('profile/', include(profile_urls)),
]