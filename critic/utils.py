"""
django-critic: utils
"""

from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template, render_to_string

from critic.modules import method_for_instance

def render(obj, **extra_context):
    t = None
    try:
        ct = ContentType.objects.get_for_model(obj)
        method = method_for_instance(obj)
    except:
        return None

    model = ct.model.lower()
    app = ct.app_label.lower()
       
    try:
        # Retreive the template from the method.
        t = get_template(method.template)
    except:
        try:
            # Retrieve the template based of off the content object
            t = get_template('critic/%s__%s.html' % (app, model)) 
        except:
            # Use the default if no template was found.
            t = get_template('critic/render.html')
            
    if not t: 
        return None
    
    # The conext that will be passed to the rendered template.
    from critic.models import RatingData
    context = {
        'obj': obj, 
        'method': method, 
        'content_type_id': ct.pk,
        'average': RatingData.objects.average(obj),
        'total': RatingData.objects.total(obj)}
        
    context.update(extra_context)
    
    # Render the template
    return render_to_string(t.name, context)
    