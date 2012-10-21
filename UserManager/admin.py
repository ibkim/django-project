from django.contrib import admin
from UserManager.models import Organization, Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'nick', 'email')
    search_fields = ('name', 'nick')
    list_filter = ('created_date',)
    filter_horizontal = ('projects', 'org',)

admin.site.register(Organization)
admin.site.register(Account, AccountAdmin)
