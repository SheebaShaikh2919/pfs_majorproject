from django.urls import path
from auth import views

urlpatterns = [
    # We can use this name in another app
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.Logout.as_view(), name='logout')
]

