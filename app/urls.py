from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginPage,name="login"),
    path('base/',views.base,name="base"),
    path('homechat/',views.homechat,name="homechat"),
    path('edit/',views.edit,name="edit"),
  
    path('logout/',views.logoutPage,name="logout"),
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    path('confirm_registration/<int:user>/', views.confirm_registration, name="confirm_registration"),
    #path('confirm/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
     path('Email/',views.Email,name="Email"),
       path('forgot_password/',views.forgot_password,name="forgot_password"),
         path('reset_password_email/',views.reset_password,name="reset_password_email"),
         
            path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
                path('confirm_reset/<int:user_id>/', views.confirm_reset, name='confirm_reset'),   
                    path('resend_confirmation/<int:user_id>/', views.resend_confirmation_code, name='resend_confirmation'),
                        path('save_message/', views.save_message, name='save_message'),
                        path('get_chat_history/', views.get_chat_history, name='get_chat_history'),
                            path('change-password/', views.change_password_view, name='change_password'),
    path('dsloimoikb/', views.friend_invitation_view, name='dsloimoikb'),
    # path('send_friend_invitation/<int:receiver_id>/', send_friend_invitation, name='send_friend_invitation'),
    path('requests/', views.friend_requests, name='friend_requests'),
    path('accept_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),

    path('dsbb/', views.friendship_view, name='dsbb'),  
    path('dskb/', views.list, name='dskb'),   
     path('friend/', views.friend, name='friend'),       
                      
]
