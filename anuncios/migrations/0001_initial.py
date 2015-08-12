# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings
import image_with_thumbnail_field


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('email', models.CharField(default='', max_length=200)),
                ('phone', models.CharField(default='', max_length=200)),
                ('text', models.TextField(default='')),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 8, 11, 10, 5, 6, 662105, tzinfo=utc))),
                ('created_ip', models.CharField(max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pic', image_with_thumbnail_field.ImageWithThumbsField(upload_to='raw')),
                ('text', models.TextField(default='')),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 8, 11, 10, 5, 6, 664412, tzinfo=utc))),
                ('created_ip', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classif', models.CharField(default='', max_length=30, db_index=True, blank=True, choices=[('gente', 'Gente'), ('hombre-busca-mujer', 'Hombre busca mujer'), ('mujer-busca-hombre', 'Mujer busca hombre'), ('hombre-busca-hombre', 'Hombre busca hombre'), ('mujer-busca-mujer', 'Mujer busca mujer'), ('encuentros-eroticos', 'Encuentros er\xf3ticos'), ('erotico-profesional', 'Er\xf3tico Profesional'), ('re-encuentros', 'Re-encuentros'), ('encontrar-amigos', 'Encontrar amigos'), ('gente-para-chatear', 'Gente para Chatear'), ('clubs-y-grupos', 'Clubs y Grupos'), ('empleo', 'Empleo'), ('administrativo', 'Administrativo'), ('compra-venta', 'Compra y Venta'), ('finanzas-contabilidad', 'Finanzas y Contabilidad'), ('atenci\xf3n-al-cliente', 'Atenci\xf3n al Cliente'), ('technico', 'T\xe9chnico'), ('ingenieria', 'Ingenier\xeda'), ('diseno-y-creativo', 'Dise\xf1o y Creativo'), ('turismo', 'Turismo'), ('publicidad-y-mercadotecnia', 'Publicidad y Mercadot\xe9cnia'), ('educacion', 'Educaci\xf3n'), ('medicina-y-sociales', 'Medicina y Sociales'), ('otros-empleos', 'Otros empleos'), ('solicitudes-de-empleo', 'Solicitudes de Empleo'), ('vivienda', 'Vivienda'), ('vender-comprar-casa', 'Venta y compra de casas'), ('vender-comprar-departamento', 'Venta y compra de departamentos'), ('rentar-casa', 'Renta de casas'), ('rentar-departamento', 'Renta de departamentos'), ('local-comercial-oficina', 'Locales Comerciales y Oficinas'), ('para-estudiantes', 'Para Estudiantes'), ('vender-y-comprar', 'Vender y Comprar'), ('coches-y-camionetas', 'Coches y Camionetas'), ('computadoras', 'Computadoras'), ('electronicos', 'Electr\xf3nicos'), ('electrodomesticos', 'Electrodom\xe9sticos'), ('celulares-y-contratos', 'Celulares y Contratos'), ('muebles', 'Muebles'), ('deportes', 'Deportes'), ('Ropa', 'Ropa'), ('coleccionables', 'Coleccionables'), ('otras', 'Otras compras y ventas'), ('gratis', 'Gratis'), ('servicios', 'Servicios'), ('hogar', 'Hogar'), ('traducciones', 'Traducciones'), ('mudanzas', 'Mudanzas'), ('internet-y-computadoras', 'Internet y Computadoras'), ('otros-servicios', 'Otros Servicios'), ('clases-y-talleres', 'Clases y Talleres'), ('idiomas', 'Idiomas'), ('computacion', 'Computaci\xf3n'), ('teatro-y-danza', 'Teatro y Danza'), ('literatura-y-pintura', 'Literatura y Pintura'), ('Otras classes', 'Otras classes')])),
                ('lat', models.FloatField(default=None, null=True)),
                ('lng', models.FloatField(default=None, null=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(max_length='')),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 8, 11, 10, 5, 6, 658565, tzinfo=utc))),
                ('updated', models.DateTimeField(default=datetime.datetime(2015, 8, 11, 10, 5, 6, 658650, tzinfo=utc))),
                ('publish', models.DateTimeField(default=datetime.datetime(2015, 8, 11, 10, 5, 6, 658707, tzinfo=utc))),
                ('expires', models.DateTimeField(default=datetime.datetime(2015, 9, 10, 10, 5, 6, 658760, tzinfo=utc))),
                ('created_ip', models.CharField(max_length=30)),
                ('updated_ip', models.CharField(max_length=30)),
                ('count_views', models.PositiveIntegerField(default=0)),
                ('count_updates', models.PositiveIntegerField(default=0)),
                ('count_messages', models.PositiveIntegerField(default=0)),
                ('is_nsfw', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='pic',
            name='post',
            field=models.ForeignKey(related_name='pics', to='anuncios.Post'),
        ),
        migrations.AddField(
            model_name='pic',
            name='user',
            field=models.ForeignKey(related_name='pics', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterIndexTogether(
            name='post',
            index_together=set([('lat', 'lng')]),
        ),
    ]
