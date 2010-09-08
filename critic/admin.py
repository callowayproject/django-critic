"""
django-critic model admin definitions
"""

from django.contrib import admin
from critic.models import RatingData
    
class RatingDataAdmin(admin.ModelAdmin):
    """
    Model admin for rating data.
    """
    list_display = ('option', 'user', 'content_object', 'updated')  
    raw_id_fields = ('user',)
    ordering = ('updated',)
    list_filter = ('option',)
    

admin.site.register(RatingData, RatingDataAdmin)