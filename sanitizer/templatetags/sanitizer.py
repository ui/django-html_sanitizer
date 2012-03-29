import django
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django import template

import bleach


ALLOWED_TAGS = getattr(settings, 'SANITIZER_ALLOWED_TAGS', [])
ALLOWED_ATTRIBUTES = getattr(settings, 'SANITIZER_ALLOWED_ATTRIBUTES', [])
STRIP = getattr(settings, 'SANITIZER_STRIP_TAGS', False)

register = template.Library()


@stringfilter
def sanitize(value):
    '''
    Sanitizes strings according to SANITIZER_ALLOWED_TAGS, SANITIZER_ALLOWED_ATTRIBUTES
    and SANITIZER_STRIP_TAGS variables in settings.

    Example usage:

    {% load sanitizer %}
    {{ post.content|santize }}

    '''
    if isinstance(value, basestring):
        value = bleach.clean(value, tags=ALLOWED_TAGS,
                             attributes=ALLOWED_ATTRIBUTES, strip=STRIP)
    return value

register.filter('sanitize', sanitize)


@stringfilter
def sanitize_allow(value, args=''):
    '''
    Strip HTML tags other than provided tags and attributes.
    Example usage:

    {% load sanitizer %}
    {{ post.body|sanitize_allow:'a, strong, img; href, src'}}
    '''
    if isinstance(value, basestring):
        allowed_tags = []
        allowed_attributes = []
        
        args = args.strip().split(';')
        if len(args) > 0:
            allowed_tags = [tag.strip() for tag in args[0].split(',')]
        if len(args) > 1:
            allowed_attributes = [attr.strip() for attr in args[1].split(',')]
            
        value = bleach.clean(value, tags=allowed_tags,
                             attributes=allowed_attributes, strip=True)
    return value

register.filter('sanitize_allow', sanitize_allow)


@register.simple_tag
def sanitize_text(value, allowed_tags=[], allowed_attributes=[], strip=False):
    """
    Template tag to sanitize string values. It accepts lists of
    allowed tags or attributes in comma separated string or list format.

    For example:

    {% load sanitizer %}
    {% sanitize_text '<a href="">bar</a> <script>alert('baz')</script>' "a,img' 'href',src' %}

    Will output:

    <a href="">bar</a> &lt;cript&gt;alert('baz')&lt;/script&gt;

    On django 1.4 you could also use keyword arguments:

    {% sanitize_text '<a href="">bar</a>' allowed_tags="a,img' allowed_attributes='href',src' strip=True %}    

    """
    if isinstance(value, basestring):
        value = bleach.clean(value, tags=allowed_tags,
                             attributes=allowed_attributes, strip=strip)
    return value