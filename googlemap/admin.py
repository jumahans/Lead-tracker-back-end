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
    list_display = ['get_freelancer', 'lead', 'called']
    list_filter = ['called']

    def get_freelancer(self, obj):
        if obj.lead and obj.lead.freelancer:
            return obj.lead.freelancer
        return '-'
    
    get_freelancer.short_description = 'Freelancer'  # Column header in admin
    get_freelancer.admin_order_field = 'lead__freelancer'  # Enables sorting by freelancer