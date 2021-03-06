#   Copyright 2011 OpenPlans and contributors
#
#   This file is part of OpenBlock
#
#   OpenBlock is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   OpenBlock is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with OpenBlock.  If not, see <http://www.gnu.org/licenses/>.
#

from django.conf.urls.defaults import *

urlpatterns = patterns('obadmin.admin.views',
    url(r'^old/$', 'index'),
    url(r'^old/schemas/$', 'schema_list'),
#    url(r'^old/schemas/(\d{1,6})/$', 'edit_schema'),
    url(r'^old/schemas/(\d{1,6})/lookups/(\d{1,6})/$', 'edit_schema_lookups'),
    url(r'^old/schemafields/$', 'schemafield_list'),
    url(r'^old/sources/$', 'blob_seed_list'),
    url(r'^old/sources/add/$', 'add_blob_seed'),
    url(r'^old/scraper-history/$', 'scraper_history_list'),
    url(r'^old/scraper-history/([-\w]{4,32})/$', 'scraper_history_schema'),
    url(r'^old/set-staff-cookie/$', 'set_staff_cookie'),
    url(r'^old/newsitems/(\d{1,6})/$', 'newsitem_details'),
    url(r'^old/geocoder-success-rates/$', 'geocoder_success_rates'),
)
