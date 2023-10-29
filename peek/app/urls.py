from . import views
from django.urls import path

urlpatterns = [
    path('', views.index,name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('post',views.post,name='post'),
    path('comment/<int:msg_id>',views.comment,name ='comment'),
    path('favorite/<int:favorite_id>',views.favorite,name='favorite'),
    path('profile/<int:user_id>',views.profile, name='profile'),
    path('message/<int:msg_id>',views.message, name='message'),

]