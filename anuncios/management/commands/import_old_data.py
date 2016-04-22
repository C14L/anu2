import csv

from dateutil.parser import parse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.timezone import utc

from anuncios.models import Post
from dtrcity.models import AltName, City


class Command(BaseCommand):
    args = ''
    help = 'Import old ads data from ~/Downloads/web1_2/es__ads.csv.'

    def handle(self, *args, **options):
        User.objects.all().delete()
        Post.objects.all().delete()
        self.import_auth_user()
        self.import_ads()

    @staticmethod
    def get_latlng(country, state, city):
        """Find latlng value for the given city id code crypt thing."""
        # country -> varchar(30)
        # state -> varchar(30)
        # city -> int(8)
        country_obj = AltName.objects.filter(type=1, slug=country)[0]
        print('Country "{}" found : {}'.format(country, country_obj.name))

        """
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
        """
        return city.lat, city.lng

    def import_ads(self):
        """
        Import 3,259,501,656 Bytes of old database "es__ads" table
        from ~/Downloads/web1_2/es__ads.csv

        ------ es__ads header fields: ------
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
        ------------------------------------
        """
        print('=== import_ads() ====================================')

        ok, skip = 0, 0
        filename = '/home/chris/Downloads/web1_2/es__ads.csv'
        print(filename)

        def _create(row):
            try:
                category = [x['slug'] for x in settings.ANUNCIOS['CATEGORIES']
                            if x['parent'] and x['old'] == row['subt']][0]
            except IndexError:
                print('no category')
                return False

            lat, lng = self.get_latlng(row['pais'], row['estado'], row['ciudad'])
            if None in (lat, lng):
                print('no latlng')
                return False

            try:
                user = User.objects.get(pk=row['user_id'])
            except User.DoesNotExist:
                user = None  # orphaned ads have no owner

            post, created = Post.objects.get_or_create(pk=row['id'])
            if not created:
                return True

            post.user = user
            post.pin = row['passwd']
            post.title = row['title']
            post.text = row['text']
            post.category = category
            post.lat, post.lng = lat, lng

            try:
                t = parse(row['time']).replace(microsecond=0).replace(tzinfo=utc)
            except AttributeError:
                t = None
            except ValueError:
                t = None
            post.created, post.updated, post.publish = t, t, t

            post.count_views = int(row['count_views'])
            post.expires_days(int(row['valid_for']))
            post.created_ip = row['ip']
            post.updated_ip = row['ip']

            post.is_nsfw = bool(row['is_adult'])
            post.is_public = True
            post.is_delete = False

        with open(filename, newline='') as fh:
            reader = csv.DictReader(fh)
            for line in reader:
                if line['is_blocked'] == '1' or line['is_deleted'] == '1':
                    continue
                if line['is_published'] != '1':
                    continue

                if _create(line):
                    ok += 1
                    print('o', end=' ', flush=True)
                else:
                    skip += 1
                    print('x', end=' ', flush=True)

        print("Done with ok: {} -- skip: {}".format(ok, skip))

    @staticmethod
    def import_auth_user():
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
        print('=== import_auth_user() ====================================')

        ok, skip = 0, 0
        filename = '/home/chris/Downloads/web1_2/es__user.csv'
        print(filename)

        def _create(row):
            if row['is_blocked'] == '1' or line['is_deleted'] == '1':
                return False  # skip blocked and deleted users
            if not row['email']:
                return False  # skip empty email/username

            try:
                user, created = User.objects.get_or_create(pk=row['id'])
            except IntegrityError as exception:
                print('For email/username: ' + row['email'])
                raise exception

            if not created:
                return True

            user.email = row['email']
            user.username = row['email']
            user.set_password(row['pass'])
            user.first_name = row['name'][:30]

            try:
                t = parse(row['lastlogin_time'])
                user.last_login = t.replace(microsecond=0).replace(tzinfo=utc)
            except AttributeError:
                user.last_login = None
            except ValueError:
                user.last_login = None

            try:
                t = parse(row['time_created'])
                user.date_joined = t.replace(microsecond=0).replace(tzinfo=utc)
            except AttributeError:
                user.date_joined = None
            except ValueError:
                user.date_joined = None

            try:
                user.save()
                return True
            except:
                return False

        with open(filename, newline='') as fh:
            reader = csv.DictReader(fh)
            for line in reader:
                if _create(line):
                    ok += 1
                    print('o', end=' ', flush=True)
                else:
                    skip += 1
                    print('x', end=' ', flush=True)

        print("Done with ok: {} -- skip: {}".format(ok, skip))


