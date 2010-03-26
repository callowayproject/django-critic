import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Avg, Max, Min, Count
from django.utils.translation import ugettext_lazy as _ 
from django.core.cache import cache

from critic import settings as csettings

class InstanceManager(models.Manager):
    def get_user_option(self, instance, obj, user):
        ctype = ContentType.objects.get_for_model(obj)
        try:
            return InstanceOptionData.objects.get(
                option__instance__pk=instance.pk,
                user__pk=user.pk,
                content_type__pk=ctype.pk,
                object_id=str(obj.pk))
        except:
            return None
    
    def get_average(self, instance, obj=None, cached=True):
        if not isinstance(instance, Instance):
            raise ValueError
        
        key = 'critic.instance.average.%s' % str(instance.pk)
        
        ctype_kwargs = {}
        if obj:
            ctype = ContentType.objects.get_for_model(obj)
            ctype_kwargs['content_type__pk'] = ctype.pk
            ctype_kwargs['object_id'] = str(obj.pk)
            
            key = '%s.%s.%s' % (key, str(ctype.pk), str(obj.pk))
            
        ret = cache.get(key)
        if ret and cached:
            return ret
        
        total, total_weight = 0, 0.0
        for option in instance.instanceoption_set.all():
            result = InstanceOptionData.objects.filter(
                option__pk=option.pk,
                option__instance__pk=instance.pk,
                **ctype_kwargs).aggregate(
                    id_count=Count('id'))['id_count']

            total_weight += float(float(result) * float(option.weight))
            total += result
        
        if total == 0:
            return total
        ret = float(float(total_weight) / float(total))
        
        cache.set(key, ret, csettings.AVERAGE_TIMEOUT)
        
        return ret
        
    def get_total(self, instance, obj=None, cached=True):
        
        if not isinstance(instance, Instance):
            raise ValueError
            
        key = 'critic.instance.total.%s' % str(instance.pk)
        
        ret = cache.get(key)
        if ret and cached:
            return ret
        
        ctype_kwargs = {}
        if obj:
            ctype = ContentType.objects.get_for_model(obj)
            ctype_kwargs['content_type__pk'] = ctype.pk
            ctype_kwargs['object_id'] = str(obj.pk)
            
            key = '%s.%s.%s' % (key, str(ctype.pk), str(obj.pk))
            
        ret = InstanceOptionData.objects.filter(
            option__instance__pk=instance.pk,
            **ctype_kwargs).count()
            
        cache.set(key, ret, csettings.TIMEOUT)
        
        return ret
            
    def get_options(self, instance):
        if not isinstance(instance, Instance):
            raise ValueError
            
        key = 'critic.instance.options.%s' % str(instance.pk)
        ret = cache.get(key)
        if ret:
            return ret
            
        ret = instance.instanceoption_set.filter(active=True).order_by('order')
        cache.set(key, ret, csettings.OPTIONS_TIMEOUT)
        
        return ret


class Instance(models.Model):
    name = models.CharField(_('Name'), max_length=255, 
        help_text=_('Name of the instance.'))
    slug = models.SlugField(_('Slug'), unique=True, 
        help_text=_('Slugified name.'))
    description = models.TextField(_('Description'), blank=True)
    multiple = models.BooleanField(_('Allow Multiple Selections'), default=False, 
        help_text=_('Will the instance allow mulitple selections by the same user?'))
    anonymous = models.BooleanField(_('Allow Anonymous Selections'), default=False, 
        help_text=_('Will the instance allow anonymous users to make a selection?'))
    created = models.DateTimeField(_('Date Created'), default=datetime.datetime.now)
    active = models.BooleanField(_('Active'), default=True)
    
    objects = InstanceManager()
    
    def __unicode__(self):
        return self.name
    

class InstanceOption(models.Model):
    instance = models.ForeignKey(Instance, verbose_name=_('Instance'), 
        help_text=_('Instance the option belongs too.'))
    name = models.CharField(_('Value'), max_length=255,
        help_text=_('The value of the option.'))
    weight = models.FloatField(default=0.0)
    order = models.IntegerField(_('Order'), default=1, 
        help_text=_('Order of the option.'))
    active = models.BooleanField(_('Acitve'), default=True)
    
    def __unicode__(self):
        return '%s - %s' % (self.instance.name, self.name)
        
    class Meta:
        ordering = ('order', )
        
    
class InstanceOptionData(models.Model):
    option = models.ForeignKey(InstanceOption, verbose_name=_('Instance Option'), 
        help_text=_('The instance option that was selected.'))
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, 
        help_text=_('The user that made a selection'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type'))
    object_id = models.CharField(_('Object ID'), max_length=255)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    updated = models.DateTimeField(_('Date Updated'), default=datetime.datetime.now)
    
    def __unicode__(self):
        return '%s - %s - (%s)' % (self.content_object, self.option.instance.name, self.option.name)
        
    def save(self, **kwargs):
        cache.delete('critic.instance.average.%s' % str(self.option.instance.pk))
        cache.delete('critic.instance.total.%s' % str(self.option.instance.pk))
        return super(InstanceOptionData, self).save(**kwargs)