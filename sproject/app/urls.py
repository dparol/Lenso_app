
from django.urls import path,include
from . import views
 

urlpatterns = [
   
    path('home',views.home,name='home'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('',views.user_login,name='user_login'),
    path('register',views.register,name='register'),
    path('admin_login_user',views.admin_login_user,name='admin_login_user'),
    path('user_delete/<int:id>',views.user_delete,name='user_delete'),
    path('user_update/<int:id>',views.user_update,name='user_update'),
    path('user_register',views.user_register,name='user_register'),
    path('admin_home',views.admin_home,name='admin_home'),
    
    


]