from django.contrib import admin
from django.urls import path,include
from core import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
=======
from DM.views import inbox,Directs
>>>>>>> 2cf088b9dfe183ee88112c64429bcd749f1f8b01

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('sign-in/', auth_views.LoginView.as_view(template_name='core/sign_in.html'), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="/")), # todo 
    path('sign-up/', views.sign_up,name='sign-up'),
<<<<<<< HEAD
    path('socialfeed/',include('socialfeed.urls')) # added to direct to social feed
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)






if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

=======
    path('socialfeed/',include('socialfeed.urls')), # added to direct to social feed
    path('message/',include('DM.urls')), # added to direct to DM
    path('profile/', views.profile_page, name='profile'),
    
]
# To display profile picture
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 2cf088b9dfe183ee88112c64429bcd749f1f8b01
