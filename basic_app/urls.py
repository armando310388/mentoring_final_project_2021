from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('counter/<pk>/',views.NewCounterRedirectView.as_view(), name='new_counter')
]
