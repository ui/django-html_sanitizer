Django Sanitizer
================

Django sanitizer is an app that provides a set of utilities to easily sanitize/escape/clean
HTML inputs in django. This app is built on top of `bleach <http://github.com/jsocol/bleach>`_,
the excellent Python HTML sanitizer.


Dependencies
------------
- `django <http://djangoproject.com/>`_: http://djangoproject.com/
- `bleach <http://github.com/jsocol/bleach>`_: http://github.com/jsocol/bleach


Installation
------------

Add ``sanitizer`` to your INSTALLED_APPS::
    
    INSTALLED_APPS = (
        # other apps
        "sanitizer",
    )


Model Usage
-----------

Similar to bleach, django sanitizer is a whitelist (only allows specified tags 
and attributes) based HTML sanitizer. Django sanitizer provides two model fields
that automatically sanitizes text values; ``SanitizedCharField`` and 
``SanitizedTextField``.

These fields accept three extra arguments:
- allowed_tags: a list of allowed HTML tags
- allowed_attributes: a list of allowed HTML attributes
- strip: a boolean indicating whether offending tags/attributes should be escaped or stripped

Here's how to use it in django models::
    
    from django.db import models
    from sanitizer.models import SanitizedCharField, SanitizedTextField

    class MyModel(models.Model):
        # Allow only <a>, <p>, <img> tags and "href" and "src" attributes
        foo = SanitizedCharField(max_length=255, allowed_tags=['a', 'p', 'img'], 
                                 allowed_attributes=['href', 'src'], strip=False)
        bar = SanitizedTextField(max_length=255, allowed_tags=['a', 'p', 'img'], 
                                 allowed_attributes=['href', 'src'], strip=False)


Form Usage
----------

Using django sanitizer in django forms is very similar to model usage::
    
    from django import forms
    from sanitizer.forms import SanitizedCharField, SanitizedTextField

    class MyForm(forms.Form):
        # Allow only <a>, <p>, <img> tags and "href" and "src" attributes
        foo = SanitizedCharField(max_length=255, allowed_tags=['a', 'p', 'img'], 
                                 allowed_attributes=['href', 'src'], strip=False)
        bar = SanitizedTextField(max_length=255, allowed_tags=['a', 'p', 'img'], 
                                 allowed_attributes=['href', 'src'], strip=False)


Template Usage
--------------

Django sanitizer provides a few differents ways of cleaning HTML in templates:

- ``escape_html`` template tag

Example usage::
    
    {% load sanitizer %}
    {% escape_html post.content "a, p, img" "href, src" %}

Assuming ``post.content`` contains the string
'<a href ="#">Example</a><script>alert("x")</script>', the above tag will
output '<a href ="#">Example</a>&lt;script&gt;alert("x")&lt;/script&gt;'


- ``strip_html`` template tag

Example usage::
    
    {% load sanitizer %}
    {% strip_html post.content "a, p, img" "href, src" %}

Assuming ``post.content`` contains the string
'<a href ="#">Example</a><script>alert("x")</script>', the above tag will
output '<a href ="#">Example</a>alert("x")'


- ``escape_html`` filter

Escapes HTML tags from string based on settings. To use this filter you need to
put these variables on settings.py:

* ``SANITIZER_ALLOWED_TAGS`` - a list of allowed tags (defaults to an empty list)
* ``SANITIZER_ALLOWED_ATTRIBUTES`` - a list of allowed attributes (defaults to an empty list)

For example if we have ``SANITIZER_ALLOWED_TAGS = ['a']``, 
``SANITIZER_ALLOWED_ATTRIBUTES = ['href']`` in settings.py, doing::
    
    {% load sanitizer %}
    {{ post.content|escape_html }}

Assuming ``post.content`` contains the string
'<a href ="#">Example</a><script>alert("x")</script>', the above filter will
output '<a href ="#">Example</a>&lt;script&gt;alert("x")&lt;/script&gt;'


- ``strip_html`` filter

Strips HTML tags from text, allowing only whitelisted tags/attributes.
To use this filter you need to put these variables on settings.py:

* ``SANITIZER_ALLOWED_TAGS`` - a list of allowed tags (defaults to an empty list)
* ``SANITIZER_ALLOWED_ATTRIBUTES`` - a list of allowed attributes (defaults to an empty list)

For example if we have ``SANITIZER_ALLOWED_TAGS = ['a']``, 
``SANITIZER_ALLOWED_ATTRIBUTES = ['href']`` in settings.py, doing::
    
    {% load sanitizer %}
    {{ post.content|strip_html }}

Assuming ``post.content`` contains the string
'<a href ="#">Example</a><script>alert("x")</script>', the above filter will
output '<a href ="#">Example</a>alert("x")'

