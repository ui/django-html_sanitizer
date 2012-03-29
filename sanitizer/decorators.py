from django import forms

import bleach


def get_sanitized_clean_func(original_clean, **kwargs):
    def fn(value):
        value = original_clean(value)
        if isinstance(value, basestring):
            value = bleach.clean(value, **kwargs)
        return value
    return fn


class sanitize(object):

    
    def __init__(self, tags=bleach.ALLOWED_TAGS,
                 attributes=bleach.ALLOWED_ATTRIBUTES, styles=[], strip=False,
                 strip_comments=True):
        self.kwargs = {
            'tags': tags,
            'attributes': attributes,
            'styles': styles,
            'strip': strip,
            'strip_comments': strip_comments,
        }


    def __call__(self, cls):
        self.actual_decorator(cls)
        return cls
        
        
    def actual_decorator(self, cls):
        fields = [(key, value) for key, value in cls.base_fields.iteritems() if isinstance(value, forms.CharField)]
        for field_name, field_object in fields:
            original_clean = getattr(field_object, 'clean')
            clean_func = get_sanitized_clean_func(original_clean, **self.kwargs)
            setattr(field_object, 'clean', clean_func)
