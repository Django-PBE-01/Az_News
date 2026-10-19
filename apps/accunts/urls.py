from django.urls import path

from apps.accunts.views import LoginView, LogoutView, ProfileView, RegistrationView


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login', ),
    path('logout/', LogoutView.as_view(), name='logout', ),
    path('register/', RegistrationView.as_view(), name='register',),
    path('profile/', ProfileView.as_view(), name='profile'),
]
