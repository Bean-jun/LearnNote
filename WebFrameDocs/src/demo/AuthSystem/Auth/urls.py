from django.urls import path
from .views import account, auth, oauth
from .apps import AuthConfig

app_name = AuthConfig.name

urlpatterns = [
    path("register/", account.RegisterView.as_view(), name="register"),
    path("login/", account.LoginView.as_view(), name="login"),
    path("auth/", auth.UserInfo.as_view(), name="auth"),
    path("oauth/", oauth.Oauth.as_view(), name="oauth"),
]
