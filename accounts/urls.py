from django.urls import path, include
from accounts import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('users/me/profile/', views.ProfileView.as_view(),name='profile-retreive-update'),
    path('activate/<str:uid>/<str:token>',
        views.ActivateUser.as_view({'post': 'activation'}),
         name='activation'),
]