from django.urls import path

from ldfinance.users import views


urlpatterns = [
    path('current/', views.CurrentUserView.as_view()),
    path('log-in/', views.LogInView.as_view()),
    path('log-out/', views.LogOutView.as_view()),
]
