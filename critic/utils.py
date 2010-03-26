from critic import settings as csettings

def get_cookie_key(instance, content_type, object_id):
    return '%s_CRITIC_%s_%s_%s' % (
        csettings.CACHE_PREFIX, 
        instance.pk, 
        content_type.id, 
        object_id)