from django.urls import path
from api.views import user_views as views

urlpatterns = [
    # Admin urls
    path('', views.get_users, name='admin-users'),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.register_User, name='register'),

    path('profile/', views.get_user_profile, name='user-profile'),
    path('profile/update/', views.update_user_profile, name='update-profile'),

]