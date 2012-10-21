from django.contrib import admin
from Repo.models import Repo

class RepoAdmin(admin.ModelAdmin):
    list_display = ('name', 'repo_path', 'creator')
    search_fields = ('name',)
    list_filter = ('name',)
    filter_horizontal = ('project_unix',)

admin.site.register(Repo, RepoAdmin)
