from django.contrib import admin
from .models import Freelancer, Lead, CallStatus

# Register your models here.
@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ["user", "skills", "created_at"]
    list_filter = ["user"]


@admin.register(Lead)
class LeaddAdmin(admin.ModelAdmin):
    list_display = ["name", 'email', 'phone', 'website', 'rating']
    list_filter = ['name']


@admin.register(CallStatus)
class CallStatusAdmin(admin.ModelAdmin):
    list_display = ["lead__freelancer", 'lead', 'called']
    # list_filter = ['freelancer']
    list_filter = ['called']