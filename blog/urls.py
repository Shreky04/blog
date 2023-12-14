from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import user_logout, subscribe

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<str:id>", views.post, name="post"),
    path("about", views.about, name="about"),
    path("services", views.services, name="services"),
    path("contact", views.contact, name="contact"),
    path('category/<str:name>', views.category, name='category'),
    path('search', views.search, name='search'),
    path("create", views.create, name="create"),
    path('logout/', user_logout, name='blog_logout'),
    path('login', LoginView.as_view(), name="blog_login"),
    path('subscribe', views.subscribe, name='subscribe'),
    path('success', views.success, name='success'),
    path('signup', views.signup, name='signup'),
    ]