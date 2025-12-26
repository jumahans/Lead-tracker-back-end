from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Freelancer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username
    
class Lead(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)  # Made optional
    rating = models.FloatField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    
    @property
    def website_status(self): 
        return self.website if self.website else "No website"
    
    @property
    def phone_status(self):
        return self.phone if self.phone else "No phone number"
    
    @property
    def email_status(self):
        return self.email if self.email else "No email"


class CallStatus(models.Model):
    lead = models.ForeignKey(Lead, on_delete = models.CASCADE, related_name='call_statuses', null=True, blank=True)
    called = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.called} - { 'called' if self.called else 'Not called'}"
    

# class CallStatus(models.Model):
#jo88414
#     STATUS_CHOICES = [
#         ('not_called', 'Not Called'),
#         ('called', 'Called'),
#         ('interested', 'Interested'),  # Fixed typo
#         ('not_interested', 'Not interested'),
#     ]

#     freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
#     lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_called")
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.freelancer.user.username} - {self.lead.name} ({self.status})"