from django.urls import path
from . import views



urlpatterns = [
    
    
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('plan/<int:pk>', views.plan, name='plan'),
    path('plan/<int:pk>', views.plan, name='plan'),
    path('register/', views.register_user, name='register'),
    path('workout/<int:pk>/', views.workout_detail, name='workout_detail'),
    

    
    
] 
] 
