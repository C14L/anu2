# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import sys
import pymysql
from django.conf import settings
from django.core.management.base import BaseCommand
from anuncios.models import Post
from dtrcity.models import AltName, City
from django.utils.timezone import utc

"""
    ----- es__ads fields: -----
    0   id                  int(10)
    1   user_id             int(10)
    2   tema                varchar(10)
    3   subt                char(2)
    4   mailhash            varchar(32)
    5   texthash            varchar(32)
    6   email               varchar(60)
    7   passwd              varchar(10)
    8   name                varchar(60)
    9   pais                varchar(30)
    10  estado              varchar(30)
    11  ciudad              int(8)
    12  title               varchar(80)
    13  text                text
    14  time                datetime
    15  ip                  varchar(15)
    16  valid_for           int(3)
    17  count_views         int(10)
    18  count_attached      int(2)
    19  is_adult            int(1)
    20  is_blocked          int(1)
    21  is_deleted          int(1)
    22  is_published        int(1)
    23  is_showemail        int(1)
    24  votes_spam          int(5)
    25  votes_illegal       int(5)
    26  votes_wrongclass    int(5)
"""

conn = pymysql.connect(user='root', passwd='pla', db='usr_web1_2', charset='utf8')
print('--> Old database connected.')

class Command(BaseCommand):
    args = ''
    help = 'Import old ads data.'

    def handle(self, *args, **options):
        self.truncate_ads()
        self.import_ads()

    def truncate_ads(self):
        all = Post.objects.all()
        print("Tuncate Post table", end=" ")
        for one in all:
            print(".", end="")
            sys.stdout.flush()
            one.delete()
        print(" done.")

    def import_ads(self):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM es__ads
            WHERE time IS NOT NULL AND is_deleted=0
            AND is_blocked=0 AND is_published=1""")
        c_old = cursor.fetchone()[0]
        c_new = Post.objects.count()
        print('--> Counted {0} old and {1} new posts.'.format(c_old, c_new))

        # Use blocks of 10,000 results for import
        step, ok, skip = 10000, 0, 0
        for lm in range(1, c_old, step):
            print('--> Fetching {} results at row {}'.format(step, lm),end=" ")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM es__ads
                WHERE is_deleted=0 AND is_blocked=0 AND is_published=1
                LIMIT %s, %s""", (lm, step))
            print("done.")
            for row in cursor:
                print('Adding post #{} ...'.format(row[0]), end=" ")
                post = Post()
                post.id = row[0]
                post.user_id = row[1]
                post.pin = row[7]
                post.title = row[12]
                post.text = row[13]
                post.created = row[14].replace(microsecond=0).replace(tzinfo=utc)
                post.updated = row[14].replace(microsecond=0).replace(tzinfo=utc)
                post.publish = row[14].replace(microsecond=0).replace(tzinfo=utc)
                post.expires_days(row[16])
                post.created_ip = row[15]
                post.updated_ip = row[15]
                post.count_views = row[17]
                post.is_nsfw = bool(row[19])
                post.is_public = True
                post.is_delete = False
                try:
                    post.category = [x['slug'] for x in
                                     settings.ANUNCIOS.CATEGORIES
                                     if x['parent'] and x['old']==row[3]][0]
                except IndexError:
                    print('has no category! SKIP')
                    continue
                post.lat, post.lng = self.get_latlng(row[9], row[10], row[11])
                if None in (post.lat, post.lng):
                    print('has no latlng value! SKIP')
                    continue
                try:
                    post.save()
                    print('OK')
                    ok += 1
                except:
                    print('SKIP')
                    skip += 1

    def get_latlng(self, country, state, city):
        """Find latlng value for the given city id code crypt thing."""
        # country -> varchar(30)
        # state -> varchar(30)
        # city -> int(8)
        cursor2 = conn.cursor()
        cursor2.execute('SELECT cityurl FROM es__ciudades WHERE id=%s', (city,))
        try:
            cityurl = cursor2.fetchone()[0]
            print("cityurl='{}'".format(cityurl), end=" ")
        except IndexError:
            print("no cityurl found", end=" ")
            return None, None
        try:
            # Use cityurl string to find a matching city AltName.slug
            city_id = AltName.objects.filter(type=3, slug=cityurl)[0].geoname_id
            print("city_id='{}'".format(city_id), end=" ")
        except IndexError:
            print("no city_id found", end=" ")
            return None, None
        try:
            city = City.objects.get(pk=city_id)
            print("city='{}'".format(city), end=" ")
        except:
            print("no City object found", end=" ")
            return None, None
        return city.lat, city.lng
