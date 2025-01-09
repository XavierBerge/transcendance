"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import SignupView
from users.views import Redirect42View, Callback42View, CheckAuthView, LoginView, LogoutView, UserInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/signup/', SignupView.as_view(), name='signup'), # route d'API defini pour enregistrer un utilisateur
	path('42/login/', Redirect42View.as_view(), name='login_42'),
    path('auth/42/callback/', Callback42View.as_view(), name='callback_42'),
	path('auth/check/', CheckAuthView.as_view(), name='check_auth'),
	path('auth/login/', LoginView.as_view(), name='login'),
	path('auth/logout/', LogoutView.as_view(), name='logout'),
	path('auth/user-info/', UserInfoView.as_view(), name='user-info'),

]