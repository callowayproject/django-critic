from django.contrib import admin
from critic.models import Instance, InstanceOption, InstanceOptionData
from django.contrib.contenttypes.models import ContentType

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'multiple', 'anonymous', 'created',)
    ordering = ('name',)
    search_fields = ('name', 'description',)
    list_filter = ('multiple', 'anonymous',)
    prepopulated_fields = {'slug': ('name',)}
    
    
class InstanceOptionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    
    
class InstanceOptionDataAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'updated',)  
    raw_id_fields = ('user',)
    

admin.site.register(Instance, InstanceAdmin)
admin.site.register(InstanceOption, InstanceOptionAdmin)
admin.site.register(InstanceOptionData, InstanceOptionDataAdmin)