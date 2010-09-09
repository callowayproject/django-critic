"""
django-critic: modules
"""
from django.contrib.contenttypes.models import ContentType
from critic import settings, register

# Holds the valid keys for the method definitions.
VALID_KEYS = ['name', 'options', 'allow_change', 'content_types']
# Holds the rating method details
METHODS = {}

class Method(object):
    def __init__(self, name, options, change):
        self.name, self.options, self.allow_change = name, options, change
        

def method_for_instance(instance):
    ctype = ContentType.objects.get_for_model(instance)
    return METHODS.get('%s.%s' % (ctype.app_label, ctype.model))

def build_methods():
    """
    Converts the settings.CRITIC_RATING_METHODS to something easier to 
    use in the code.
    """
    for method in settings.RATING_METHODS:
        # Valid that the keys for the method are valid.
        for k in method.keys():
            if not k in VALID_KEYS:
                raise KeyError(
                    "critic: %s is not a valid key." % k)
                    
        for ct_string in method.get('content_types', []):
            ctype = None
            try:
                app_label, model = ct_string.split('.')
                ctype = ContentType.objects.get(app_label__iexact=app_label, 
                    model__iexact=model)
            except ContentType.DoesNotExist, Exception:
                raise Exception(
                    "critic: %s is not a valid content type." % ct_string)
            
            if ct_string in METHODS:
                raise KeyError(
                    "critic: %s is already assigned." % ct_string)
                    
            METHODS[ct_string] = Method(
                name=method.get('name', ''), 
                options=method.get('options', []),
                change=method.get('allow_change', settings.ALLOW_CHANGE))
                
            # Registrer method to model
            register(ctype.model_class(), 
                critic_descriptor_attr=settings.RATING_ATTR)
                