from django.urls import path

from .api import AdminLocationAPI, AdminMeterAPI, AdminUserAPI, AdminDetailUserAPI

urlpatterns = [
    path('admin/locations', AdminLocationAPI.as_view()),
    path('admin/meters', AdminMeterAPI.as_view()),
    path('admin/users', AdminUserAPI.as_view()),
    path('admin/users/<int:pk>', AdminDetailUserAPI.as_view())
]