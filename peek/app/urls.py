from . import views
from django.urls import path

app_name ='accounts'


urlpatterns = [
    path('', views.index,name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

]