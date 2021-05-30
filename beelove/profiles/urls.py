from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import render

urlpatterns = [
    path('', views.home,name='home'),
    path('signup/', views.register_view , name='signup'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('Questionnaire/', views.Questionnaire , name='Questionnaire'),
    path('createque/', views.CreateQue , name='createque'),
    path('updateque/', views.updateque , name='updateque'),
    path('reports/', views.reports , name='reports'),
    # path('ProfilePage/<userid>/', views.ProfilePage , name='Profile'),
    re_path('ProfilePage/(?P<userId>[0-9]+)/cropImage/', views.crop_image , name='cropImage'),
    re_path('ProfilePage/(?P<userId>[0-9]+)/edit/', views.Edit , name='EditProfile'),
    re_path('ProfilePage/(?P<userId>[0-9]+)/', views.ProfilePage, name='Profile'),
    # re_path('ProfilePage/(?P<userid>[0-9]+)/edit/', views.EditProfilePage, name='EditProfile'),
    # re_path('EditProfilePage/', views.EditProfilePage, name='EditProfile'),
    path('Chat/', views.Chat , name='Chat'),
    path('aboutus/', views.aboutus , name='aboutus'),
    path('contactus/', views.contactus , name='contactus'),
    path('price/', views.price , name='price'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='profiles/password_change_done.html'),name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='profiles/password_change.html'),name='password_change'),
    path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='profiles/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='profiles/password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'),name='password_reset_complete'),

]


urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)