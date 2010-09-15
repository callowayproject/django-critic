"""
Custom managers for Django models registered with the critic application.
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType

from critic.models import RatingData
from critic.modules import method_for_instance

class ModelRatingManager(models.Manager):
    """
    A manager for retrieving rating data for a particular instance.
    """
    instance = None
    def get_query_set(self):
        """
        Default queryset.
        """
        ctype = Content.objects.get_for_model(self.instance)
        return RatingData.objects.filter(content_type_id=ctype.pk, 
            object_id=self.instance.pk)
    
    def add(self, usr, opt):
        """
        Add a new rating for the instance.
        """
        return RatingData.objects.add(self.instance, usr, opt)
        
    def change(self, usr, opt):
        """
        Update the rating for the user for a instance.
        """
        return RatingData.objects.change(self.instance, usr, opt)
        
    def user_rating(self, usr):
        """
        Retreive the selection the specified user made for the instance.
        """
        return RatingData.objects.user_rating(self.instance, usr)
    
    @property
    def average(self):
        """
        Retrieve the average rating for the instance.
        """
        return RatingData.objects.average(self.instance)
        
    @property
    def total(self):
        """
        Retrieve the total ratings for the instance. opt (option) is optional.
        """
        return RatingData.objects.total(self.instance)
        
    @property
    def data(self):
        """
        Retrieves a break down of totals and percentages for each option.
        """
        method = method_for_instance(self.instance)
        return_data = {}
        for opt in method.options:
            opt_total = RatingData.objects.total(self.instance, opt=opt)
            
            if opt_total == 0 or self.total == 0:
                perc = 0
            else:
                perc = float(opt_total) / float(self.total)
                
            return_data[str(opt)] = {
                'percentage': int(perc * 100),
                'total': opt_total}
                
        return return_data
        

class RatingDescriptor(object):
    """
    A descriptor which provides access to a ``ModelRatingManager`` for
    model classes and simple retrieval and updating of rating
    data for model instances.
    """
    def __get__(self, instance, owner):
        if instance:
            manager = ModelRatingManager()
            manager.instance = instance
            return manager
        return None

    def __set__(self, instance, value):
        # Cannot add/change the rating in this way. 
        # Use .add(..)  or .change(..)
        raise NotImplementedError

    def __delete__(self, instance):
        # Ratings should not be deleted.
        raise NotImplementedError
        