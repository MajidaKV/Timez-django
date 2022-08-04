from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home,name="home"),
    path('register/', views.register,name="register"),
    path('login/', views.login,name="login"),
    path('logout/', views.logout,name="logout"),
    
    path('dashboard/', views.dashboard, name="dashboard"),
    path('my_orders/', views.my_orders, name="my_orders"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('changepassword/', views.change_password, name="change_password"),
    path('order_detail/<int:order_id>/', views.order_detail, name="order_detail"),
    # path('cancel_order/<int:id>/',views.cancel_order,name='cancel_order'),
    
    path('activate/<uidb64>/<token>/',views.activate, name="activate"),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name="resetpassword_validate"),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]    