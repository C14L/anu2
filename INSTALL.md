
mysql -uroot -ppla -e "CREATE DATABASE anuncios2"
./manage.py migrate
./manage.py createsuperuser
./manage.py import_cities
./manage.py import_users
./manage.py import_posts

