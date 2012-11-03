from django import forms
from django.db import models
from django.test import TestCase
from django.test.utils import override_settings

from sanitizer.templatetags.sanitizer import (sanitize, sanitize_allow,
    escape_html, strip_filter, strip_html)
from .forms import SanitizedCharField as SanitizedFormField
from .models import SanitizedCharField, SanitizedTextField


ALLOWED_TAGS = ['a']
ALLOWED_ATTRIBUTES = ['href', 'style']
ALLOWED_STYLES = ['width']


class TestingModel(models.Model):
    test_field = SanitizedCharField(max_length=255, allowed_tags=ALLOWED_TAGS, 
        allowed_attributes=ALLOWED_ATTRIBUTES, allowed_styles=ALLOWED_STYLES)


class TestingTextModel(models.Model):
    test_field = SanitizedTextField(allowed_tags=ALLOWED_TAGS, 
        allowed_attributes=ALLOWED_ATTRIBUTES, allowed_styles=ALLOWED_STYLES)


class TestForm(forms.Form):
    test_field = SanitizedFormField(allowed_tags=['a'], 
    allowed_attributes=['href', 'style'], allowed_styles=['width'])


class SanitizerTest(TestCase):

    @override_settings(SANITIZER_ALLOWED_TAGS=['a'])
    def test_sanitize(self):
        """ Test sanitize function in templatetags """
        self.assertEqual(sanitize('test<script></script>'), 
            'test&lt;script&gt;&lt;/script&gt;')

    def test_strip_filter(self):
        """ Test strip_html filter """
        self.assertEqual(strip_filter('test<script></script>'), 'test')

    def test_sanitize_allow(self):
        """ Test sanitize_allow function in templatetags """
        self.assertEqual(sanitize_allow('test<script></script><br>', 'br'), 'test<br>')
        self.assertEqual(sanitize_allow('test<script></script><br/>', 'br'), 'test<br>')
        self.assertEqual(sanitize_allow('<a href="">test</a>', 'a'), '<a>test</a>')
        self.assertEqual(sanitize_allow('<a href="">test</a>', 'a; href'), '<a href="">test</a>')


    def test_SanitizedCharField(self):
        TestingModel.objects.create(test_field='<a href="" style="width: 200px; height: 400px">foo</a><em>bar</em>')
        test = TestingModel.objects.latest('id')
        self.assertEqual(test.test_field, '<a href="" style="width: 200px;">foo</a>&lt;em&gt;bar&lt;/em&gt;')


    def test_SanitizedTextField(self):
        TestingTextModel.objects.create(test_field='<a href="" style="width: 200px; height: 400px">foo</a><em>bar</em>')
        test = TestingTextModel.objects.latest('id')
        self.assertEqual(test.test_field, '<a href="" style="width: 200px;">foo</a>&lt;em&gt;bar&lt;/em&gt;')

    def test_SanitizedFormField(self):
        html = '<a href="" style="width: 200px; height: 400px">foo</a><em class=""></em>'
        form = TestForm({ 'test_field': html })
        form.is_valid()
        self.assertEqual(form.cleaned_data['test_field'],
                         '<a href="" style="width: 200px;">foo</a>&lt;em class=""&gt;&lt;/em&gt;')

    def test_escape_html(self):
        html = '<a href="" class="" style="width: 200px; height: 400px">foo</a><em></em>'
        self.assertEqual(escape_html(html, allowed_tags='a', 
            allowed_attributes='href,style', allowed_styles='width'),
            '<a href="" style="width: 200px;">foo</a>&lt;em&gt;&lt;/em&gt;')
        self.assertEqual(escape_html(html, allowed_tags=['a'], 
            allowed_attributes=['href', 'style'], allowed_styles=['width']),
            '<a href="" style="width: 200px;">foo</a>&lt;em&gt;&lt;/em&gt;')
    
    def test_strip_html(self):
        html = '<a href="" class="" style="width: 200px; height: 400px">foo</a><em></em>'
        self.assertEqual(strip_html(html, allowed_tags='a', 
            allowed_attributes='href,style', allowed_styles='width'),
            '<a href="" style="width: 200px;">foo</a>')
        self.assertEqual(strip_html(html, allowed_tags=['a'], 
            allowed_attributes=['href', 'style'], allowed_styles=['width']),
            '<a href="" style="width: 200px;">foo</a>')
