from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'school_name', 'is_inspector']

admin.site.register(UserProfile, UserProfileAdmin)


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'sf_code', 'inspector_name', 'inspection_date', 'completed')
    list_filter = ('completed', 'inspection_date')
    search_fields = ('school_name', 'sf_code', 'inspector_name')
