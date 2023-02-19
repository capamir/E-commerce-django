from django.urls import path
from api.views import user_views as views

urlpatterns = [
    # Admin urls
    path('', views.get_users, name='admin-get-users'),
    path('<int:user_id>/', views.get_user_by_id, name='admin-get-user'),
    path('update/<int:user_id>/', views.update_user, name='admin-update-user'),
    path('delete/<int:user_id>/', views.delete_user, name='admin-delete-user'),

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.register_User, name='register'),

    path('profile/', views.get_user_profile, name='user-profile'),
    path('profile/update/', views.update_user_profile, name='update-profile'),

]