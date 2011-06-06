"""
django-critic: template tags
"""

from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from critic.models import RatingData
from critic.utils import render

register = Library()


class GetUserRating(Node):
    def __init__(self, obj, varname):
        self.obj, self.varname = obj, varname

    def render(self, context):
        context[self.varname] = None
        try:
            obj = Variable(self.obj).resolve(context)
        except:
            return ""

        request = None
        try:
            request = Variable("request").resolve(context)
        except:
            return ""

        if request.user and request.user.is_authenticated():
            context[self.varname] = RatingData.objects.user_rating(
                obj, request.user)

        return ""


def do_user_rating(parser, token):
    """
    {% critic_user_rating object as varname %}
    {% critic_user_rating story as user_rating %}
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc != 4:
        raise TemplateSyntaxError('Tag %s takes three arguments.' % argv[0])
    if argv[2] != "as":
        raise TemplateSyntaxError('Second argument must be "as" for tag %s' %
            argv[0])

    return GetUserRating(argv[1], argv[3])


class RenderNode(Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        try:
            obj = Variable(self.obj).resolve(context)
        except:
            return ""

        extra_context = {}
        try:
            # Retrieve the request.user
            user = Variable('user').resolve(context)
            if user.is_authenticated():
                extra_context['user_rating'] = RatingData.objects.user_rating(
                    obj, user)
            # Add csrf_token to form
            csrf = Variable('csrf_token').resolve(context)
            extra_context['csrf_token'] = csrf
        except Exception:
            pass

        return render(obj, **extra_context)


def do_render(parser, token):
    """
    {% critic_render obj %}
    {% critic_render entry %}
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc != 2:
        raise TemplateSyntaxError('Tag %s takes one argument.' % argv[0])

    return RenderNode(obj=argv[1])


class RenderURLNode(Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        try:
            obj = Variable(self.obj).resolve(context)
        except:
            return ''
        try:
            ctype = ContentType.objects.get_for_model(obj)
        except:
            return ''

        return reverse('critic_rating_render', args=[ctype.pk, obj.pk])


def do_render_url(parser, token):
    """
    {% critic_render_url [object] %}
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc != 2:
        raise TemplateSyntaxError('Tag %s takes one argument.' % argv[0])

    return RenderURLNode(obj=argv[1])

register.tag("critic_user_rating", do_user_rating)
register.tag("critic_render", do_render)
register.tag("critic_render_url", do_render_url)
