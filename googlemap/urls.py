from django.urls import path 
from . import views

urlpatterns  = [
    path('create-user/', views.CreateUser.as_view(), name='create-user'),
    path('get-business-details/', views.get_bussines_details, name='get-business-details'),
    path('freelancer-details/', views.Freelancer_details, name='freelancer-details'),
    path('list-leads/', views.list_leads, name='list-leads'),  # ✅ fixed 
    path('delete-lead/<int:pk>/', views.delete_lead.as_view(), name='delete-lead'),
    path('profile-details/', views.get_profile_details, name='profile-details'),
    path('call-status/<int:lead_id>/', views.toggle_call_status, name='call-status'),
    path('update-profile-details/', views.update_user_profile_details, name='update-profile-details'),
]
