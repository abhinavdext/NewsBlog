from django.urls import path
from . import views

urlpatterns = [

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'notifications/',
        views.notifications,
        name='notifications'
    ),

    path(
        'notifications/<int:notification_id>/read/',
        views.mark_notification_read,
        name='mark_notification_read'
    ),

    path(
        'notifications/mark-all-read/',
        views.mark_all_notifications_read,
        name='mark_all_notifications_read'
    ),
]