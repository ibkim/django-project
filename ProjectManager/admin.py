from django.contrib import admin
from ProjectManager.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('created_date',)
    filter_horizontal = ('members', 'repos',)

admin.site.register(Project, ProjectAdmin)
