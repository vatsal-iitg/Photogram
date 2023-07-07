from DM.views import inbox , Directs, SendDirect, UserSearch
from django.urls import path

urlpatterns = [
    path('inbox/', inbox, name="inbox"),
    path('directs/<username>', Directs, name="directs"),
    path('send/', SendDirect, name="send-directs"),
    path('search/', UserSearch, name="search-users"),
    
]