
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'edit/<int:link_id>/',
        views.edit_link,
        name='edit_link'
    ),

    path(
        'delete/<int:link_id>/',
        views.delete_link,
        name='delete_link'
    ),

    path(
        '@<str:username>/',
        views.profile,
        name='profile'
    ),

    # Короткий код должен оставаться последним маршрутом!
    path(
        '<str:code>/',
        views.short_redirect,
        name='short_redirect'
    ),
]
