# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import pymysql
import sys
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import utc

"""
row[2].replace(microsecond=0).replace(tzinfo=utc)
    ----- es__user fields: -----
    0   id              int(10)
    1   pass            varchar(20)
    2   email           varchar(80)
    3   name            varchar(100)
    4   mailhash        varchar(32)
    5   time_offset     int(2)
    6   datetime_format varchar(30)
    7   date_short      varchar(30)
    8   date_long       varchar(30)
    9   ip_created      varchar(15)
    10  time_created    datetime
    11  lastlogin_ip    varchar(15)
    12  lastlogin_time  datetime
    13  time            datetime
    14  ip              varchar(15)
    15  is_blocked      tinyint(1)
    16  is_deleted      tinyint(1)
    17  is_admin        tinyint(1)
"""

conn = pymysql.connect( user='root', passwd='pla', db='usr_web1_2', charset='utf8')
print('--> Old database connected.')

class Command(BaseCommand):
    args = ''
    help = 'Import old user account data.'

    def handle(self, *args, **options):
        #self.truncate_user()
        self.import_auth_user()

    def truncate_user(self):
        all = User.objects.all()
        print("Tuncate User table", end=" ")
        for one in all:
            print(".", end="")
            sys.stdout.flush()
            one.delete()
        print(" done.")

    def import_auth_user(self):
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM es__user')
        c_old = cursor.fetchone()[0]
        c_new = User.objects.count()
        print('--> Counted {0} old and {1} new users.'.format(c_old, c_new))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM es__user')
        ok, skip = 0, 0

        for row in cursor:
            print('Adding user #{} "{}" "{}"...'.format(row[0], row[2], row[3]), end=" ")
            user = User()
            user.id = row[0]
            user.username = row[2]
            user.set_password(row[1])
            user.email = row[2]
            user.first_name = row[3][0:30]
            try: user.last_login = row[12].replace(microsecond=0).replace(tzinfo=utc)
            except AttributeError: user.last_login = None
            try: user.date_joined = row[10].replace(microsecond=0).replace(tzinfo=utc)
            except AttributeError: user.date_joined = None
            try:
                user.save()
            except:
                print('User #{} "{}" could not be saved.'.format(row[0], row[2]))
                skip += 1
                continue
            print('OK')
            ok += 1
        print("OK: {} -- SKIP: {}".format(ok, skip))
        print("Done.")
