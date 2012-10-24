from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from UserManager.models import Organization, Account

class UserProfileInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'profile'

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
    inlines = [UserProfileInline,]

admin.site.register(Organization)
admin.site.unregister(User)
admin.site.register(User, AccountAdmin)
