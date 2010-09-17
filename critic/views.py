"""
django-critic views.
"""
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from critic.models import RatingData
from critic.utils import render

POST_ADD_FIELDS = ['content_type_id', 'object_id', 'option']

@login_required
@never_cache
def add_rating(request, redirect_field_name='next'):
    """
    Add a user rating. Needs to be sent via POST.
    """
    if not request.method == 'POST':
        raise Http404
    
    if request.is_ajax():
        # Return a normal HttpResponse if the request is ajax.
        response = HttpResponse()
    else:
        # Retreive the redirect url.
        next_url = request.GET.get(redirect_field_name, '/')
        # Redirect to next_url if this is a normal request.
        response = HttpResponseRedirect(next_url)
    
    # Retreive the data.
    data_dict = request.POST
    
    try:
        # Retrieve three values from either the POST or GET.
        # These values should be integers
        ct_id = int(data_dict.get('content_type_id'))
        obj_id = int(data_dict.get('object_id'))
        option = int(data_dict.get('option'))
    except Exception:
        raise Http404
        
    # Retreive the content type instance
    ctype = get_object_or_404(ContentType, pk=ct_id)
    # Retreive the object instance.
    obj = get_object_or_404(ctype.model_class(), pk=obj_id)
    
    # Add the rating.
    RatingData.objects.add(obj, request.user, option)
    
    return response
    
def render_rating(request, content_type_id, object_id):
    """
    Returns the rendered rating template.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    
    # The only extra context we need to retreive is the user rating, if
    # the user is authenticated.
    user_rating = None
    if request.user.is_authenticated():
        user_rating = RatingData.objects.user_rating(obj, request.user)
    
    rendered_content = render(obj, **{'user_rating': user_rating})
    return HttpResponse(rendered_content)
    
def user_rating_json(request, content_type_id, object_id):
    """
    Returns the user option for the supplied content type instance.
    """
    # Retreive the content type instance
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    
    # Retreive the object instance.
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    
    if request.user.is_authenticated():
        user_rating = RatingData.objects.user_rating(obj, request.user)
    else:
        user_rating = None
    
    json = simplejson.dumps({'user_rating': user_rating})
    return HttpResponse(json, mimetype='application/json')
    
def rating_data_json(request, content_type_id, object_id, option=None):
    """
    Returns the average, total and rounded average for a vote.
    Can also return the average, total and rounded average for a given object.
    """
    # Retreive the content type instance
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    
    # Retreive the object instance.
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    
    # Make sure option is None or an integer
    if option:
        option = int(option)
    
    # Retreive the average and total for the instance.
    average = RatingData.objects.average(obj) or 0
    total = RatingData.objects.total(obj, option) or 0
    
    json = simplejson.dumps({'average': average, 'total': total, 
        'average_rounded': int(round(float(average)))})
    return HttpResponse(json, mimetype='application/json')
    
    