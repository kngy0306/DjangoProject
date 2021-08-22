from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # viewsモジュールのsignUpViewをインスタンス化する
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # viewsモジュールのsignUpSuccessViewをインスタンス化する
    path('signup_success', views.SignUpSuccessView.as_view(), name='signup_success'),
    # ログイン django.contrib.auth.views.LoginViewをインスタンス化する
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # ログアウト django.contrib.auth.views.logoutViewをインスタンス化する
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
