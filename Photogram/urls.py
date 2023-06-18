from django.contrib import admin
from django.urls import path,include
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('sign-in/', auth_views.LoginView.as_view(template_name='core/sign_in.html'), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="/")), # todo 
    path('sign-up/', views.sign_up,name='sign-up'),
    path('socialfeed/',include('socialfeed.urls')) # added to direct to social feed
]
