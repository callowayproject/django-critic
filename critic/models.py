"""
django-critic models.
"""
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Count, Avg
from django.utils.translation import ugettext_lazy as _ 

from critic.modules import method_for_instance

class RatingManager(models.Manager):
    """
    The rating manager.
    """
    def add(self, obj, usr, opt):
        """
        Add/modify a user option.
        """
        # Retreive the method and content type for the supplied instance.
        method = method_for_instance(obj)        
        ctype = ContentType.objects.get_for_model(obj)
        
        # Check if obj and usr exist and if opt is a valid option.
        if not obj or not usr or not opt in method.options:
            return None
        
        try:
            # Get the RatingData instance for the supplied arguments
            data = self.get(content_type__pk=ctype.pk, object_id=obj.pk, 
                user__pk=usr.pk)
            # If something was found, and the method allows changes and
            # if the supplied opt is different then the current option,
            # then save the new option for the usr.
            if method.allow_change and data.option != opt:
                data.option = opt
                data.save()
        except RatingData.DoesNotExist:
            # If no record was found, create a new one
            data = self.create(content_type=ctype, object_id=obj.pk, user=usr)
        return data
        
    def change(self, obj, usr, opt):
        """
        Change the rating. This will simply call the .add(...) method to 
        make the change.
        """
        return self.add(obj, usr, opt)

    def user_option(self, obj, usr):
        """
        Returns the option for the supplied user
        """
        extra_kwargs = {}

        if not obj or not usr:
            return None
        
        ctype = ContentType.objects.get_for_model(obj)
        try:
            return self.get(content_type__pk=ctype.pk, object_id=obj.pk,
                **extra_kwargs).option
        except RatingData.DoesNotExist:
            return None
        
    
    def average(self, obj):
        """
        Returns the average rating for the supplied object.
        """
        ctype = ContentType.objects.get_for_model(obj)
        return self.objects.filter(content_type__pk=ctype.pk,
            object_id=obj.pk).aggregate(Avg('option'))['option__avg']
        
    def total(self, obj, opt=None):
        """
        Returns the total # of ratings for the supplied object. Can also
        be supplied for a option to get the total for a certain option.
        """
        ctype = ContentType.objects.get_for_model(obj)
        method = method_for_instance(obj)
        
        # If a option is specifed, add the option to the query.
        opt_kwargs = {}
        if opt in method.options:
            opt_kwargs = {'option': opt}
            
        return self.objects.filter(content_type__pk=ctype.pk, 
            object_id=obj.pk, **opt_kwargs).aggregate(
                Count('id'))['id__count']
        
    
class RatingData(models.Model):
    """
    User data for a rating. Holds the object in which the user 
    has made a rating.
    """
    user = models.ForeignKey(User, verbose_name=_('User'), null=True)
    option = models.IntegerField()
    content_type = models.ForeignKey(ContentType, 
        verbose_name=_('Content Type'))
    object_id = models.CharField(_('Object ID'), max_length=255)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    updated = models.DateTimeField(_('Date Updated'), 
        default=datetime.datetime.now)
    
    objects = RatingManager()
            
       
# Build the methods     
from critic.modules import build_methods
build_methods()