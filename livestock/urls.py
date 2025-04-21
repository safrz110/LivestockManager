from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('animals/', views.animal_list, name='animal_list'),
    path('animals/add/', views.add_animal, name='add_animal'),
    path('animals/breeds/', views.get_breeds_by_species, name='get_breeds_by_species'),
    path('api/generate-tag/', views.generate_tag, name='generate_tag'),
    path('api/find-user/', views.find_user, name='find_user'),
    path('profile/', views.profile, name='profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('profile/preferences/', views.update_preferences, name='update_preferences'),
    path('ownership/', views.ownership, name='ownership'),
    path('transfer/<int:transfer_id>/<str:action>/', views.process_transfer, name='process_transfer'),

    # Notification related URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),

    # Health record URLs
    path('health-records/', views.health_records, name='health_records'),
    path('health-records/add/<int:animal_id>/', views.add_health_record, name='add_health_record'),
    path('health-records/edit/<int:record_id>/', views.edit_health_record, name='edit_health_record'),
    path('health-records/delete/<int:record_id>/', views.delete_health_record, name='delete_health_record'),
    path('api/health-record/<int:record_id>/', views.get_health_record, name='get_health_record'),

    # User management
    path('users/', views.user_management, name='user_management'),
    path('api/toggle-user-verification/<int:user_id>/', views.toggle_user_verification, name='toggle_user_verification'),
    path('api/user-details/<int:user_id>/', views.get_user_details, name='get_user_details'),
    path('api/disable-user/<int:user_id>/', views.disable_user, name='disable_user'),
    path('api/toggle-user-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('users/toggle-verification/<int:user_id>/', views.toggle_user_verification_form, name='toggle_user_verification'),

    # Support system
    path('support/', views.support_request, name='support_request'),
    path('support/requests/', views.support_requests_list, name='support_requests_list'),
    path('support/requests/<int:request_id>/', views.support_request_detail, name='support_request_detail'),

    # New URL pattern
    path('get-breeds/<int:species_id>/', views.get_breeds_for_species, name='get_breeds_for_species'),
]
