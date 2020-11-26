from django.urls import path
from django.conf.urls import url
from login import views
app_name='login'
urlpatterns = [
    url(r'^$', views.login, name='login1'),
]
