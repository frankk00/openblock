#   Copyright 2007,2008,2009,2011 Everyblock LLC, OpenPlans, and contributors
#
#   This file is part of ebpub
#
#   ebpub is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   ebpub is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with ebpub.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Unit tests for db app.
"""

from django.core import urlresolvers
from django.test import TestCase
from ebpub.db.models import NewsItem, Attribute
import datetime

class ViewTestCase(TestCase):
    "Unit tests for views.py."
    fixtures = ('crimes',)

    def test_search__bad_schema(self):
        url = urlresolvers.reverse('ebpub.db.views.search', args=['kaboom'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_search__no_query(self):
        url = urlresolvers.reverse('ebpub.db.views.search', args=['crime'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://testserver/crime/')
        response = self.client.get(url + '?type=alert')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://testserver/crime/')

    def test_search(self):
        url = urlresolvers.reverse('ebpub.db.views.search', args=['crime'])
        response = self.client.get(url + '?q=228 S. Wabash Ave.')
        self.assertEqual(response.status_code, 200)
        assert 'location not found' in response.content.lower()
        # TODO: load a fixture with some locations and some news?


    def test_newsitem_detail(self):
        # response = self.client.get('')
        pass

    def test_location_redirect(self):
        # redirect to neighborhoods by default
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'http://testserver/locations/neighborhoods/')

    def test_location_type_detail(self):
        # response = self.client.get('')
        pass

    def test_location_detail(self):
        # response = self.client.get('')
        pass

    def test_schema_detail(self):
        response = self.client.get('/crime/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)

    def test_schema_xy_detail(self):
        # response = self.client.get('')
        pass

class TestSchemaFilterView(TestCase):

    fixtures = ('crimes',)

    def test_filter_choices(self):
        url = urlresolvers.reverse('schema-filter', args=['crime', ''])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filter_detail(self):
        # response = self.client.get('')
        pass

    def test_filter_detail_month(self):
        # response = self.client.get('')
        pass

    def test_filter_detail_day(self):
        # response = self.client.get('')
        pass

class DatabaseExtensionsTestCase(TestCase):
    "Unit tests for the custom ORM stuff in models.py."
    fixtures = ('crimes',)

    def testAttributesLazilyLoaded(self):
        # Attributes are retrieved lazily the first time you access the
        # `attributes` attribute.

        # Turn DEBUG on and reset queries, so we can keep track of queries.
        # This is hackish.
        from django.conf import settings
        from django.db import connection
        connection.queries = []
        settings.DEBUG = True

        ni = NewsItem.objects.get(id=1)
        self.assertEquals(ni.attributes['case_number'], u'HM609859')
        self.assertEquals(ni.attributes['crime_date'], datetime.date(2006, 9, 19))
        self.assertEquals(ni.attributes['crime_time'], None)
        self.assertEquals(len(connection.queries), 3)

        connection.queries = []
        settings.DEBUG = False

    def testSetAllAttributesNonDict(self):
        # Setting `attributes` to something other than a dictionary will raise
        # ValueError.
        ni = NewsItem.objects.get(id=1)
        def setAttributeToNonDict():
            ni.attributes = 1
        self.assertRaises(ValueError, setAttributeToNonDict)

    def testSetAllAttributes1(self):
        # Attributes can be set by assigning a dictionary to the `attributes`
        # attribute. As soon as `attributes` is assigned-to, the UPDATE query
        # is executed in the database.
        ni = NewsItem.objects.get(id=1)
        self.assertEquals(ni.attributes['case_number'], u'HM609859')
        ni.attributes = dict(ni.attributes, case_number=u'Hello')
        self.assertEquals(Attribute.objects.get(news_item__id=1).varchar01, u'Hello')

    def testSetAllAttributes2(self):
        # Setting attributes works even if you don't access them first.
        ni = NewsItem.objects.get(id=1)
        ni.attributes = {
            u'arrests': False,
            u'beat_id': 214,
            u'block_id': 25916,
            u'case_number': u'Hello',
            u'crime_date': datetime.date(2006, 9, 19),
            u'crime_time': None,
            u'domestic': False,
            u'is_outdated': True,
            u'location_id': 66,
            u'police_id': None,
            u'status': u'',
            u'type_id': 97
        }
        self.assertEquals(Attribute.objects.get(news_item__id=1).varchar01, u'Hello')

    def testSetAllAttributesNull(self):
        # If you assign to NewsItem.attributes and the dictionary
        # doesn't include a value for every field, a None/NULL will be
        # inserted for values that aren't represented in the
        # dictionary.
        ni = NewsItem.objects.get(id=1)
        ni.attributes = {u'arrests': False}
        ni = NewsItem.objects.get(id=1)
        self.assertEquals(ni.attributes['arrests'], False)
        self.assertEquals(ni.attributes['beat_id'], None)
        self.assertEquals(ni.attributes['block_id'], None)
        self.assertEquals(ni.attributes['case_number'], None)
        self.assertEquals(ni.attributes['crime_date'], None)
        self.assertEquals(ni.attributes['crime_time'], None)
        self.assertEquals(ni.attributes['domestic'], None)
        self.assertEquals(ni.attributes['is_outdated'], None)
        self.assertEquals(ni.attributes['location_id'], None)
        self.assertEquals(ni.attributes['police_id'], None)
        self.assertEquals(ni.attributes['status'], None)
        self.assertEquals(ni.attributes['type_id'], None)

    def testSetSingleAttribute1(self):
        # Setting a single attribute will result in an immediate query setting
        # just that attribute.
        ni = NewsItem.objects.get(id=1)
        self.assertEquals(ni.attributes['case_number'], u'HM609859')
        ni.attributes['case_number'] = u'Hello'
        self.assertEquals(Attribute.objects.get(news_item__id=1).varchar01, u'Hello')

    def testSetSingleAttribute2(self):
        # Setting single attributes works even if you don't access them first.
        ni = NewsItem.objects.get(id=1)
        ni.attributes['case_number'] = u'Hello'
        self.assertEquals(Attribute.objects.get(news_item__id=1).varchar01, u'Hello')

    def testSetSingleAttribute3(self):
        # Setting a single attribute will result in the value being cached.
        ni = NewsItem.objects.get(id=1)
        self.assertEquals(ni.attributes['case_number'], u'HM609859')
        ni.attributes['case_number'] = u'Hello'
        self.assertEquals(ni.attributes['case_number'], u'Hello')

    def testSetSingleAttribute4(self):
        # Setting a single attribute will result in the value being cached, even
        # if you don't access the attribute first.
        ni = NewsItem.objects.get(id=1)
        ni.attributes['case_number'] = u'Hello'
        self.assertEquals(ni.attributes['case_number'], u'Hello')

    def testSetSingleAttributeNumQueries(self):
        # When setting an attribute, the system will only use a single query --
        # i.e., it won't have to retrieve the attributes first simply because
        # code accessed the NewsItem.attributes attribute.

        # Turn DEBUG on and reset queries, so we can keep track of queries.
        # This is hackish.
        from django.conf import settings
        from django.db import connection
        connection.queries = []
        settings.DEBUG = True

        ni = NewsItem.objects.get(id=1)
        ni.attributes['case_number'] = u'Hello'
        self.assertEquals(len(connection.queries), 3)

        connection.queries = []
        settings.DEBUG = False

    def testBlankAttributes(self):
        # If a NewsItem has no attributes set, accessing
        # NewsItem.attributes will return an empty dictionary.
        Attribute.objects.filter(news_item__id=1).delete()
        ni = NewsItem.objects.get(id=1)
        self.assertEquals(ni.attributes, {})

    def testSetAttributesFromBlank(self):
        # When setting attributes on a NewsItem that doesn't have
        # attributes yet, the underlying implementation will use an
        # INSERT statement instead of an UPDATE.
        Attribute.objects.filter(news_item__id=1).delete()
        ni = NewsItem.objects.get(id=1)
        ni.attributes = {
            u'arrests': False,
            u'beat_id': 214,
            u'block_id': 25916,
            u'case_number': u'Hello',
            u'crime_date': datetime.date(2006, 9, 19),
            u'crime_time': None,
            u'domestic': False,
            u'is_outdated': True,
            u'location_id': 66,
            u'police_id': None,
            u'status': u'',
            u'type_id': 97
        }
        self.assertEquals(Attribute.objects.get(news_item__id=1).varchar01, u'Hello')

    def testSetSingleAttributeFromBlank(self):
        # When setting a single attribute on a NewsItem that doesn't have
        # attributes yet, the underlying implementation will use an INSERT
        # statement instead of an UPDATE.
        Attribute.objects.filter(news_item__id=1).delete()
        ni = NewsItem.objects.get(id=1)
        ni.attributes['case_number'] = u'Hello'
        self.assertEquals(Attribute.objects.get(news_item__id=1).varchar01, u'Hello')

    def testAttributeFromBlankSanity(self):
        # Sanity check for munging attribute data from blank.
        Attribute.objects.filter(news_item__id=1).delete()
        ni = NewsItem.objects.get(id=1)
        self.assertEquals(ni.attributes, {})
        ni.attributes['case_number'] = u'Hello'
        self.assertEquals(ni.attributes['case_number'], u'Hello')
        self.assertEquals(Attribute.objects.get(news_item__id=1).varchar01, u'Hello')
