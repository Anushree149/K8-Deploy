
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('forgot_pass/',views.forgot_pass,name='forgot_pass'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('reset',views.reset,name='reset'),
    path('reset_password/<uidb64>/<token>',views.resetpassword,name='resetpassword'),

]
