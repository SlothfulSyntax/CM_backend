from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class UserModelAdmin(UserAdmin):
    pass

# admin.site.register(JobListing)



@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    # Define which fields to display in the Django Admin for JobListing
    list_display = [ 'id','company_name', 'position', 'apply_link', 'image',]
    search_fields = ['company_name', 'position']
    list_filter = ['position']