from django.conf import settings
from django.db import models
from django.utils.encoding import smart_unicode

import bleach


class SanitizedCharField(models.CharField):
    
    def __init__(self, allowed_tags=[], allowed_attributes=[],
                 strip=False, *args, **kwargs):
        self._sanitizer_allowed_tags = allowed_tags
        self._sanitizer_allowed_attributes = allowed_attributes
        self._sanitizer_strip = strip
        super(SanitizedCharField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(SanitizedCharField, self).to_python(value)
        value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
            attributes=self._sanitizer_allowed_attributes, strip=self._sanitizer_strip)
        return smart_unicode(value)


class SanitizedTextField(models.TextField):
    
    def __init__(self, allowed_tags=[], allowed_attributes=[], strip=False,
                 *args, **kwargs):
        self._sanitizer_allowed_tags = allowed_tags
        self._sanitizer_allowed_attributes = allowed_attributes
        self._sanitizer_strip = strip
        super(SanitizedTextField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(SanitizedTextField, self).to_python(value)
        value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
            attributes=self._sanitizer_allowed_attributes, strip=self._sanitizer_strip)
        return smart_unicode(value)

    def get_prep_value(self, value):
        value = super(SanitizedTextField, self).get_prep_value(value)
        value = bleach.clean(value, tags=self._sanitizer_allowed_tags,
            attributes=self._sanitizer_allowed_attributes, strip=self._sanitizer_strip)
        return value


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    rules = [
      (
        (SanitizedCharField, SanitizedTextField),
        [],
        {
            "allowed_tags": ["_sanitizer_allowed_tags", {}],
            "allowed_attributes": ["_sanitizer_allowed_attributes", {}],
            "strip": ["_sanitizer_strip", {}],
        },
      )
    ]

    add_introspection_rules(rules, ["^sanitizer\.models\.SanitizedCharField"])
    add_introspection_rules(rules, ["^sanitizer\.models\.SanitizedTextField"])
