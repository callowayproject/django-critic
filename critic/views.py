from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType

from critic.models import Instance, InstanceOption, InstanceOptionData
from critic.utils import get_cookie_key

def make_vote(request, instance_id, option_id, content_type_id, object_id):
    redirect_to = request.GET.get('r', '/')
    if request.is_ajax():
        response = HttpResponse()
    else:
        response = HttpResponseRedirect(redirect_to)
        
    try:
        ins = Instance.objects.get(pk=instance_id, active=True)
        opt = InstanceOption.objects.get(pk=option_id, active=True)
        ctype = ContentType.objects.get(pk=content_type_id)
    except (Instance.DoesNotExist, InstanceOption.DoesNotExist, ContentType.DoesNotExist):
        return response
        
    d = InstanceOptionData()
    d.option = opt
    d.content_type = ctype
    d.object_id = object_id
    
    if request.user.is_authenticated():
        d.user = request.user
        if not ins.multiple:
            try:
                data = InstanceOptionData.objects.get(
                    option__instance__pk=instance_id,
                    content_type__pk=content_type_id,
                    object_id=object_id,
                    user__pk=request.user.pk)
                data.option = opt
                data.save()
                return response
            except InstanceOptionData.DoesNotExist:
                pass
    elif ins.anonymous:
        key = get_cookie_key(ins, ctype, object_id)
        if not key in request.COOKIES.keys():
            response.set_cookie(key=str(key), value=str(option_id))
        elif not ins.multiple:
            return response
    else:
        return response

    d.save()
    return response
    
    
def json_data(request, instance_id, content_type_id, object_id):
    try:
        ins = Instance.objects.get(pk=instance_id, active=True)
        ctype = ContentType.objects.get(pk=content_type_id)
    except (Instance.DoesNotExist, ContentType.DoesNotExist):
        return HttpResponse()
        
    try:
        obj = ctype.get_object_for_this_type(id=object_id)
    except:
        return HttpResponse()
        
    avg = Instance.objects.get_average(ins, obj, cached=False)
    total = Instance.objects.get_total(ins, obj, cached=False)
    
    json = simplejson.dumps({'avg': avg, 'total': total, 'rounded_avg': int(round(avg))})
    return HttpResponse(json, mimetype='application/json')
    
    