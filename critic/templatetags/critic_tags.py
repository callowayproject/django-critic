from django.template import Library, Node, TemplateSyntaxError, Variable, resolve_variable, VariableDoesNotExist
from django.contrib.contenttypes.models import ContentType
from critic.models import Instance, InstanceOption, InstanceOptionData
from critic.utils import get_cookie_key

register = Library()

class GetOptions(Node):
    def __init__(self, name, varname):
        self.name, self.varname = name, varname
        
    def render(self, context):
        try:
            ins = Instance.objects.get(slug__iexact=self.name)
        except Instance.DoesNotExist:
            return ''
        
        opts = Instance.objects.get_options(ins)
        context[self.varname] = opts
        return ''
    
    
class GetAvg(Node):
    def __init__(self, name, obj, varname):
        self.name, self.obj, self.varname = name, obj, varname
        
    def render(self, context):
        self.obj = Variable(self.obj).resolve(context)
        try:
            ins = Instance.objects.get(slug__iexact=self.name)
        except Instance.DoesNotExist:
            return ''
            
        avg = Instance.objects.get_average(ins, self.obj)
        context[self.varname] = {'raw': avg, 'rounded': int(round(avg))}
        return ''
        
    
class GetTotal(Node):
    def __init__(self, name, obj, varname):
        self.name, self.obj, self.varname = name, obj, varname
        
    def render(self, context):
        self.obj = Variable(self.obj).resolve(context)
        try:
            ins = Instance.objects.get(slug__iexact=self.name)
        except Instance.DoesNotExist:
            context[self.varname] = '0'
        
        context[self.varname] = Instance.objects.get_total(ins, self.obj)
        return ''
        
class GetOptionUrl(Node):
    def __init__(self, obj):
        self.obj =  obj
        
    def render(self, context):
        self.obj = Variable(self.obj).resolve(context)
        
        ctype = ContentType.objects.get_for_model(self.obj)
        ret = '/%s/%s/' % (ctype.pk, self.obj.pk)
        return ret
        
        
class GetUserOption(Node):
    def __init__(self, name, obj, varname):
        self.name, self.obj, self.varname = name, obj, varname
        
    def render(self, context):
        context[self.varname] = None
        try:
            ins = Instance.objects.get(slug__iexact=self.name)
        except Instance.DoesNotExist:
            return ""
            
        try:
            obj = Variable(self.obj).resolve(context)
        except:
            return ""
            
        request = None
        try:
            request = Variable("request").resolve(context)
        except:
            pass
            
        data = None
        if request and request.user and request.user.is_authenticated:
            data = Instance.objects.get_user_option(ins, obj, request.user)
            
            ctype = ContentType.objects.get_for_model(obj)
            key = get_cookie_key(ins, ctype, obj.pk)
            if key in request.COOKIES:
                print request.COOKIES[key]
                try:
                    data = InstanceOptionData.objects.get(
                        content_type__pk=ctype.pk,
                        object_id=str(obj.pk),
                        option__pk=request.COOKIES[key])
                except:
                    pass
                
        if data:
            context[self.varname] = data
        return ""
        
        
def do_get_options(parser, token):
    """
        {% get_critic_options [name] as [varname] %}
        {% get_critic_options default as options %}
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc != 4:
        raise TemplateSyntaxError, "Tag %s takes three argument." % argv[0]
    else:
        if argv[2] != 'as':
            raise TemplateSyntaxError, "The second argument must be 'as'."
    return GetOptions(argv[1], argv[3])
    
def do_get_avg(parser, token):
    """
        {% get_critic_avg [name] for [object] as [varname] %}
        {% get_critic_avg default for story as avg %}
    """
    argv = token.contents.split()
    argc = len(argv)
    
    if argc == 6:
        if argv[2] != 'for':
            raise TemplateSyntaxError, "Second argument for tag %s, has to be 'for'." % argv[0]
        elif argv[4] != 'as':
            raise TemplateSyntaxError, "Fourth argument for tag %s, has to be 'as'." % argv[0]
    else:
        raise TemplateSyntaxError, "Tag %s takes either 4 arguments." % argv[0]

    return GetAvg(argv[1], argv[3], argv[5])
    
def do_get_total(parser, token):
    """
        {% get_critic_total [name] for [object] as [varname] %}
        {% get_critic_total default for story as varname %}
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc != 6:
        raise TemplateSyntaxError, "Tag %s takes five arguments." % argv[0]
    else:
        if argv[2] != 'for':
            raise TemplateSyntaxError, "The second argument must be 'for' for tag %s." % argv[0]
        if argv[4] != 'as':
            raise TemplateSyntaxError, "The fourth argument must be 'as' for tag %s." % argv[0]
    return GetTotal(argv[1], argv[3], argv[5])
    
    
def critic_add_url(content_object):
    """
        Returns the content object information in the format of a url
        IE: /74/23123123/
    """
    
    ctype = ContentType.objects.get_for_model(content_object)
    return '%s/%s' % (ctype.pk, content_object.pk)
    
def do_get_user_option(parser, token):
    """
    {% get_critic_user_option name object as varname %}
    {% get_critic_user_option name story as useropt %}
    """
    argv = token.contents.split()
    argc = len(argv)
    
    if argc != 5:
        raise TemplateSyntaxError, "Tag %s takes four arguments." % argv[0]
    if argv[3] != "as":
        raise TemplateSyntaxError, 'Thrid argument must be "as" for tag %s' % argv[0]
        
    return GetUserOption(argv[1], argv[2], argv[4])
        
    
register.tag("get_critic_options", do_get_options)
register.tag("get_critic_avg", do_get_avg)
register.tag("get_critic_total", do_get_total)
register.tag("get_critic_user_option", do_get_user_option)

register.simple_tag(critic_add_url)