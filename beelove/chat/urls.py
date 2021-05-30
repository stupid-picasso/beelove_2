from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path('chat/', views.chat,name='chat'),
]

urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)