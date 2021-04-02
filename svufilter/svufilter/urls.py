from django.contrib import admin
from django.urls import path,include
from users import views as viewsUser
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('classifier.urls'),),
    path('register/',viewsUser.registerUser,name = 'register'),
    path('login/',viewsUser.loginUser,name='login'),
    path('logout/',viewsUser.logoutUser,name='logout'),
    path('check/',viewsUser.TestMsg,name='check'),
    path('chage_password/',viewsUser.changePassword,name='change_password')
]
