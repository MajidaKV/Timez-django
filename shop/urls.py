from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home,name="home"),
    path('register/', views.register,name="register"),
    path('login/', views.login,name="login"),
    path('logout/', views.logout,name="logout"),
    path('activate/<uidb64>/<token>/',views.activate, name="activate"),
]    