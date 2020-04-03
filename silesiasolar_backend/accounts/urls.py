from django.urls import path, include
from knox import views as knox_views
from .api import RegisterAPI, LoginAPI, UserAPI, AdminUserAPI, AdminDetailUserAPI


urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view(), name='knox-logout'),

    path('userinfo', UserAPI.as_view()),
    path('admin/users', AdminUserAPI.as_view()),
    path('admin/users/<int:pk>', AdminDetailUserAPI.as_view())

]
