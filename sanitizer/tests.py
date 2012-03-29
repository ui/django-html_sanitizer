from django import forms
from django.db import models
from django.test import TestCase

from sanitizer.templatetags.sanitizer import sanitize, sanitize_allow, sanitize_text
from .forms import SanitizedCharField as SanitizedFormField
from .models import SanitizedCharField, SanitizedTextField


ALLOWED_TAGS = ['a']
ALLOWED_ATTRIBUTES = ['href']


class TestingModel(models.Model):
    test_field = SanitizedCharField(max_length=255, allowed_tags=ALLOWED_TAGS, 
        allowed_attributes=ALLOWED_ATTRIBUTES)


class TestingTextModel(models.Model):
    test_field = SanitizedTextField(allowed_tags=ALLOWED_TAGS, 
        allowed_attributes=ALLOWED_ATTRIBUTES)    


class TestForm(forms.Form):
    test_field = SanitizedFormField(allowed_tags=['a'], allowed_attributes=['href'])


class SanitizerTest(TestCase):


    def test_sanitize(self):
        """ Test sanitize function in templatetags """
        self.assertEqual(sanitize('test<script></script>'), 'test')
        self.assertEqual(sanitize('<a href="">test</a>'), '<a href="">test</a>')


    def test_sanitize_allow(self):
        """ Test sanitize_allow function in templatetags """
        self.assertEqual(sanitize_allow('test<script></script><br>', 'br'), 'test<br>')
        self.assertEqual(sanitize_allow('test<script></script><br/>', 'br'), 'test<br>')
        self.assertEqual(sanitize_allow('<a href="">test</a>', 'a'), '<a>test</a>')
        self.assertEqual(sanitize_allow('<a href="">test</a>', 'a; href'), '<a href="">test</a>')


    def test_SanitizedCharField(self):
        TestingModel.objects.create(test_field='<a href="">foo</a><em>bar</em>')
        test = TestingModel.objects.latest('id')
        self.assertEqual(test.test_field, '<a href="">foo</a>&lt;em&gt;bar&lt;/em&gt;')


    def test_SanitizedTextField(self):
        TestingTextModel.objects.create(test_field='<a href="">foo</a><em>bar</em>')
        test = TestingTextModel.objects.latest('id')
        self.assertEqual(test.test_field, '<a href="">foo</a>&lt;em&gt;bar&lt;/em&gt;')

    def test_SanitizedFormField(self):
        html = '<a href="">foo</a><em class=""></em>'
        form = TestForm({ 'test_field': html })
        form.is_valid()
        self.assertEqual(form.cleaned_data['test_field'],
                         '<a href="">foo</a>&lt;em class=""&gt;&lt;/em&gt;')

    def test_sanitize_text(self):
        html = '<a href="" class="">foo</a><em></em>'
        self.assertEqual(sanitize_text(html, allowed_tags='a', allowed_attributes='href', strip=False),
                         '<a href="">foo</a>&lt;em&gt;&lt;/em&gt;')
        self.assertEqual(sanitize_text(html, allowed_tags=['a'], allowed_attributes=['href'], strip=False),
                         '<a href="">foo</a>&lt;em&gt;&lt;/em&gt;')
        self.assertEqual(sanitize_text(html, allowed_tags='a', allowed_attributes='href', strip=True),
                         '<a href="">foo</a>')
        self.assertEqual(sanitize_text(html, allowed_tags=['a'], allowed_attributes=['href'], strip=True),
                         '<a href="">foo</a>')