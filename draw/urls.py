from django.urls import path
from . import views

app_name = "draw"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('detail/', views.detail, name='detail'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('adddraw/', views.add_new_draw, name='add_new_draw'),
    path('addpower/', views.add_power, name='add_power'),
    path('<int:draw_id>/draw/', views.draw_begin, name='draw'),
    path('sendemail/', views.send_register_email, name='send_email'),
    path('forget/', views.forget_psw, name='forget'),
    path('change/', views.change_psw, name='change'),
    path('adminreg/', views.admin_reg, name='admin_reg'),
    path('log/', views.update_log, name='update_log'),
    path('addLike/', views.add_likes, name='add_likes'),
    path('user/<str:username>/', views.user_main, name='user_main'),
]
