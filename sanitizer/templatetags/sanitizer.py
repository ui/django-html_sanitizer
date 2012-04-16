import django
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django import template

import bleach


ALLOWED_TAGS = getattr(settings, 'SANITIZER_ALLOWED_TAGS', [])
ALLOWED_ATTRIBUTES = getattr(settings, 'SANITIZER_ALLOWED_ATTRIBUTES', [])

register = template.Library()


@stringfilter
def sanitize(value):
    '''
    Sanitizes strings according to SANITIZER_ALLOWED_TAGS and
    SANITIZER_ALLOWED_ATTRIBUTES variables in settings.

    Example usage:

    {% load sanitizer %}
    {{ post.content|escape_html }}

    '''
    if isinstance(value, basestring):
        value = bleach.clean(value, tags=ALLOWED_TAGS,
                             attributes=ALLOWED_ATTRIBUTES, strip=False)
    return value

register.filter('escape_html', sanitize)


@stringfilter
def strip_filter(value):
    '''
    Strips HTML tags from strings according to SANITIZER_ALLOWED_TAGS and
    SANITIZER_ALLOWED_ATTRIBUTES variables in settings.

    Example usage:

    {% load sanitizer %}
    {{ post.content|strip_html }}

    '''
    if isinstance(value, basestring):
        value = bleach.clean(value, tags=ALLOWED_TAGS,
                             attributes=ALLOWED_ATTRIBUTES, strip=True)
    return value

register.filter('strip_html', strip_filter)


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
def escape_html(value, allowed_tags=[], allowed_attributes=[]):
    """
    Template tag to sanitize string values. It accepts lists of
    allowed tags or attributes in comma separated string or list format.

    For example:

    {% load sanitizer %}
    {% escape_html '<a href="">bar</a> <script>alert('baz')</script>' "a,img' 'href',src' %}

    Will output:

    <a href="">bar</a> &lt;cript&gt;alert('baz')&lt;/script&gt;

    On django 1.4 you could also use keyword arguments:

    {% escape_html '<a href="">bar</a>' allowed_tags="a,img' allowed_attributes='href',src' %}    

    """
    if isinstance(value, basestring):
        value = bleach.clean(value, tags=allowed_tags,
                             attributes=allowed_attributes, strip=False)
    return value


@register.simple_tag
def strip_html(value, allowed_tags=[], allowed_attributes=[]):
    """
    Template tag to strip html from string values. It accepts lists of
    allowed tags or attributes in comma separated string or list format.

    For example:

    {% load sanitizer %}
    {% strip_html '<a href="">bar</a> <script>alert('baz')</script>' "a,img' 'href',src' %}

    Will output:

    <a href="">bar</a> alert('baz');

    On django 1.4 you could also use keyword arguments:

    {% strip_html '<a href="">bar</a>' allowed_tags="a,img' allowed_attributes='href',src' %}    

    """
    if isinstance(value, basestring):
        value = bleach.clean(value, tags=allowed_tags,
                             attributes=allowed_attributes, strip=True)
    return value