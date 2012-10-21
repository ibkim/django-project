from django.contrib import admin
from ProcessManager.models import ReqCategory, WBSCategory, Requirement, WBS

class WBSAdmin(admin.ModelAdmin):
        list_display = ('name', 'description')
        search_fields = ('name', 'description')
        list_filter = ('name',)
        filter_horizontal = ('reqs', 'resources',)
                    
admin.site.register(ReqCategory)
admin.site.register(WBSCategory)
admin.site.register(Requirement)
admin.site.register(WBS, WBSAdmin)

