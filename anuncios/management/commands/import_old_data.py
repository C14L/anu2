import csv
import sys

from dateutil.parser import parse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils.timezone import utc

from anuncios.models import Post, make_username
from dtrcity.models import AltName, Country, City
from toolbox import force_int


class Command(BaseCommand):
    args = ''
    help = 'Import old ads data from ~/Downloads/web1_2/es__ads.csv.'
    city_tr = dict()
    location_not_found = dict()

    def handle(self, *args, **options):
        try:
            self.build_city_tr()
            # User.objects.all().delete()
            Post.objects.all().delete()
            # self.import_auth_user()
            self.import_ads()
            self.done()
        except KeyboardInterrupt:
            self.done()
            sys.exit()

    def done(self):
        print('.')
        print('='*80)
        for k in self.location_not_found.keys():
            print('{:05d} - {}'.format(self.location_not_found[k], k))
        print('='*80)

    def build_city_tr(self):
        """Reads the list of cities and city id numbers."""
        filename = '/home/chris/Downloads/web1_2/es__ciudades.csv'
        with open(filename, newline='') as fh:
            reader = csv.DictReader(fh)
            for line in reader:
                self.city_tr[line['id']] = line['cityurl']

    def count_location_not_found(self, name):
        self.location_not_found[name] = self.location_not_found.get(name, 0) + 1

    def get_city_name(self, city):
        try:
            int(city)
            return self.city_tr[city]
        except ValueError:
            return city

    def get_latlng(self, country, state, city):
        """Find latlng value for the given city id code crypt thing."""
        lang = settings.LANGUAGE_CODE
        # country -> varchar(30)
        # state -> varchar(30)
        # city -> int(8)

        # 1. Find the country
        country = slugify(country).lower()
        # Some manual fixing
        if country == 'costarica': country = 'costa-rica'
        if country == 'elsalvador': country = 'el-salvador'

        # print('--> For country "{}", language "{}" ...'.format(country, lang))
        countries = AltName.objects.filter(type=1, language=lang)
        # print('Found {} countries in Altname ...'.format(countries.count()))
        countries_f = countries.filter(slug__exact=country)
        # print('Found {} exact matches ...'.format(countries_f.count()))

        if countries_f.count() < 1:
            # Try to find partial matches
            countries_f = countries.filter(slug__contains=country)
            # print('Found {} cointain countries: {} ...'
            #       .format(countries_f.count(), countries_f))

        if countries_f.count() < 1:
            # Still no match, giving up
            print('No location found for country: {}'.format(country))
            self.count_location_not_found(country)
            return None

        country = Country.objects.get(pk=countries_f[0].geoname_id)
        country_slug = countries_f[0].slug
        # print('Found country object {} ...'.format(country))

        # 2. Find the city in that country
        # ---------------------------------
        city = self.get_city_name(city)  # get the old slug
        city = slugify(city).lower()  # make sure its slugified

        # Some manual fixing
        if country_slug == 'venezuela' and city == 'distrito-metropolitano-de-caracas':
            city = 'caracas'
        if country_slug == 'costa-rica' and city == 'central-san-jose':
            city = 'san-jose'
        if country_slug == 'colombia' and city == 'distrito-capital':
            city = 'bogota'
        if country_slug == 'mexicio' and city == 'chapultepec':
            city = 'distrito-federal'
        if country_slug == 'republica-dominicana' and city == 'distrito-nacional':
            city = 'santo-domingo'

        # print('--> For city "{}", language "{}" ...'.format(city, lang))
        cities = AltName.objects.filter(type=3, language=lang, country=country)
        # print('Found {} cities in Altname ...'.format(cities.count()))
        cities_f = cities.filter(slug__exact=city)
        # print('Found {} exact matches: {}'.format(cities_f.count(), cities_f))

        if cities_f.count() < 1:
            # Try to find partial matches
            cities_f = cities.filter(slug__contains=city)
            # print('Found {} cointain cities: {} ...'
            #       .format(cities_f.count(), cities_f))

        if cities_f.count() < 1:
            # Still no match, giving up
            s = '{}, {}'.format(city, country_slug)
            print('No location found for city: {}'.format(s))
            self.count_location_not_found(s)
            return None

        city = City.objects.get(pk=cities_f[0].geoname_id)
        # print('City: {}, {} @ {}/{}'.format(city, city.country,
        #                                     city.lat, city.lng))
        return city

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
                print('Skip because: no category')
                return False

            try:
                user = User.objects.get(username=row['email'][:30])
            except User.DoesNotExist:
                user = None  # orphaned ads have no owner

            post, created = Post.objects.get_or_create(pk=row['id'])
            if not created:
                print('Skip because: already exists pk='+row['id'])
                return True  # already previously imported

            city = self.get_latlng(row['pais'], row['estado'], row['ciudad'])

            post.user = user
            post.pin = row['passwd'][:5]
            post.title = row['title'][:200]
            post.text = row['text'] or ''
            post.category = category

            if city:
                post.lat = city.lat
                post.lng = city.lng
                post.city = city
                post.city_name = city.tr_name
                post.region_name = city.region.tr_name
                post.country_name = city.country.tr_name
            else:
                post.city_name = self.get_city_name(row['ciudad'])
                post.region_name = row['estado']
                post.country_name = row['pais']

            try:
                t = parse(row['time']).replace(microsecond=0).replace(tzinfo=utc)
            except AttributeError:
                t = None
            except ValueError:
                t = None
            post.created, post.updated, post.publish = t, t, t

            post.count_views = force_int(row['count_views'], 0, 0)
            post.expires_days = force_int(row['valid_for'], 90, 30, 365)
            post.created_ip = (row['ip'] or '')[:30]
            post.updated_ip = (row['ip'] or '')[:30]

            post.is_nsfw = (row['is_adult'] == '1')
            post.is_public = (row['is_published'] == '1')
            post.is_delete = (row['is_blocked'] == '1' or
                              row['is_deleted'] == '1')
            post.save()
            return True

        with open(filename, newline='') as fh:
            reader = csv.DictReader(fh)
            while True:
                try:
                    line = next(reader)
                except UnicodeDecodeError:
                    continue
                except StopIteration:
                    break

                if _create(line):
                    ok += 1
                    print('o', end=' ', flush=True)
                else:
                    skip += 1
                    print('x', end=' ', flush=True)

        print("Done with ok: {} -- skip: {}".format(ok, skip))

    def import_auth_user(self):
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
            if row['is_blocked'] == '1' or row['is_deleted'] == '1':
                return False  # skip blocked and deleted users
            if not row['email']:
                return False  # skip empty email/username

            username = make_username(row['email'])
            user, created = User.objects.get_or_create(username=username)
            if not created:
                return False  # user with that email/username already exists

            user.email = row['email']
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


