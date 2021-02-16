from django.urls import path

from ldfinance.users import views


app_name = "users"

urlpatterns = [
    path("current/", views.CurrentUserView.as_view(), name="current"),
    path("log-in/", views.LogInView.as_view(), name="log-in"),
    path("log-out/", views.LogOutView.as_view(), name="log-out"),
]
