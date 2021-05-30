from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import render

urlpatterns=[
    path('match_request/',views.send_match_request,name="send_match_request"),
    re_path('match_request/(?P<userId>[0-9]+)/',views.match_requests,name="match_requests_view"),
    re_path('accept_match_request/(?P<match_request_id>[0-9]+)/',views.accept_match_request,name="accept-match-request"),
]