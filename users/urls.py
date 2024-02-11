
from django.urls import path
from users.views import register_view,login_view,logout_view,profileview


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profileview.as_view(), name='profile'),
]
