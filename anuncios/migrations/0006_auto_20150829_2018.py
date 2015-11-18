# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0005_auto_20150812_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='created_ip',
            field=models.CharField(default='', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='pic',
            name='text',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='pic',
            name='user',
            field=models.ForeignKey(related_name='pics', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(default='', max_length=30, db_index=True, blank=True, choices=[('gente', 'Gente'), ('hombre-busca-mujer', 'Hombre busca mujer'), ('mujer-busca-hombre', 'Mujer busca hombre'), ('hombre-busca-hombre', 'Hombre busca hombre'), ('mujer-busca-mujer', 'Mujer busca mujer'), ('encuentros-eroticos', 'Encuentros er\xf3ticos'), ('erotico-profesional', 'Er\xf3tico Profesional'), ('re-encuentros', 'Re-encuentros'), ('encontrar-amigos', 'Encontrar amigos'), ('gente-para-chatear', 'Gente para Chatear'), ('clubs-y-grupos', 'Clubs y Grupos'), ('empleo', 'Empleo'), ('administrativo', 'Administrativo'), ('compra-venta', 'Compra y Venta'), ('finanzas-contabilidad', 'Finanzas y Contabilidad'), ('atenci\xf3n-al-cliente', 'Atenci\xf3n al Cliente'), ('technico', 'T\xe9chnico'), ('ingenieria', 'Ingenier\xeda'), ('diseno-y-creativo', 'Dise\xf1o y Creativo'), ('turismo', 'Turismo'), ('publicidad-y-mercadotecnia', 'Publicidad y Mercadot\xe9cnia'), ('educacion', 'Educaci\xf3n'), ('medicina-y-sociales', 'Medicina y Sociales'), ('otros-empleos', 'Otros empleos'), ('solicitudes-de-empleo', 'Solicitudes de Empleo'), ('vivienda', 'Vivienda'), ('vender-comprar-casa', 'Venta y compra de casas'), ('vender-comprar-departamento', 'Venta y compra de departamentos'), ('rentar-casa', 'Renta de casas'), ('rentar-departamento', 'Renta de departamentos'), ('local-comercial-oficina', 'Locales Comerciales y Oficinas'), ('para-estudiantes', 'Para Estudiantes'), ('vender-y-comprar', 'Vender y Comprar'), ('coches-y-camionetas', 'Coches y Camionetas'), ('computadoras', 'Computadoras'), ('electronicos', 'Electr\xf3nicos'), ('electrodomesticos', 'Electrodom\xe9sticos'), ('celulares-y-contratos', 'Celulares y Contratos'), ('muebles', 'Muebles'), ('deportes', 'Deportes'), ('Ropa', 'Ropa'), ('coleccionables', 'Coleccionables'), ('otras', 'Otras compras y ventas'), ('gratis', 'Gratis'), ('servicios', 'Servicios'), ('hogar', 'Hogar'), ('traducciones', 'Traducciones'), ('mudanzas', 'Mudanzas'), ('internet-y-computadoras', 'Internet y Computadoras'), ('otros-servicios', 'Otros Servicios'), ('clases-y-talleres', 'Clases y Talleres'), ('idiomas', 'Idiomas'), ('computacion', 'Computaci\xf3n'), ('teatro-y-danza', 'Teatro y Danza'), ('literatura-y-pintura', 'Literatura y Pintura'), ('otras-classes', 'Otras classes')]),
        ),
    ]
