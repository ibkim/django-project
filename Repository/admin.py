from django.contrib import admin
from Repository.models import Repository

class RepoAdmin(admin.ModelAdmin):
    list_display = ('reponame', 'repo_path', 'creator')
    search_fields = ('reponame',)
    list_filter = ('reponame',)
    #filter_horizontal = ('project_unix',)

admin.site.register(Repository, RepoAdmin)
