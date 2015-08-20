# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

class ANUNCIOS:

    CATEGORIES = [

        {
            'slug': 'gente',
            'old': None,
            'parent': None,
            'title': 'Gente',
            'descr': ('Anuncios para encontrar nuevos amigos. Encontrar '
                      'pareja o alguien con quién chatear. Reencontrar '
                      'viejos amigos de la escuelas que perdiste de vista.'),
        }, {
            'slug': 'hombre-busca-mujer',
            'old': 'ha',
            'parent': 'gente',
            'title': 'Hombre busca mujer',
            'descr': 'Anuncios de hombres que están buscando a mujeres.',
            'is_nsfw': True,
        }, {
            'slug': 'mujer-busca-hombre',
            'old': 'hb',
            'parent': 'gente',
            'title': 'Mujer busca hombre',
            'descr': 'Anuncios de mujeres que buscan a un hombre.',
            'is_nsfw': True,
        }, {
            'slug': 'hombre-busca-hombre',
            'old': 'hc',
            'parent': 'gente',
            'title': 'Hombre busca hombre',
            'descr': 'Anuncios de hombres que buscan a otros hombres.',
            'is_nsfw': True,
        }, {
            'slug': 'mujer-busca-mujer',
            'old': 'hd',
            'parent': 'gente',
            'title': 'Mujer busca mujer',
            'descr': 'Anuncios de mujeres buscando a otras mujeres.',
            'is_nsfw': True,
        }, {
            'slug': 'encuentros-eroticos',
            'old': 'he',
            'parent': 'gente',
            'title': 'Encuentros eróticos',
            'descr': ('Anuncios para encontrar personas para una relación '
                     'íntima.'),
            'is_nsfw': True,
        }, {
            'slug': 'erotico-profesional',
            'old': 'hf',
            'parent': 'gente',
            'title': 'Erótico Profesional',
            'descr': ('Si lo vendes por dinero, esta es la sección para tu '
                      'anuncio.'),
            'is_nsfw': True,
        }, {
            'slug': 're-encuentros',
            'old': 'hg',
            'parent': 'gente',
            'title': 'Re-encuentros',
            'descr': ('Si perdiste de vista a viejos amigos de la escuela, '
                      'aquí puedes poner un anuncio de búsqueda.'),
        }, {
            'slug': 'encontrar-amigos',
            'old': 'hh',
            'parent': 'gente',
            'title': 'Encontrar amigos',
            'descr': 'Encontrar nuevos amigos para salir y divertirse.',
        }, {
            'slug': 'gente-para-chatear',
            'old': 'hi',
            'parent': 'gente',
            'title': 'Gente para Chatear',
            'descr': 'Anuncios para encontrar a personas con quien chatear.',
        }, {
            'slug': 'clubs-y-grupos',
            'old': 'hk',
            'parent': 'gente',
            'title': 'Clubs y Grupos',
            'descr': 'Anuncios de clubs y grupos, grupos de música.',
        },
        ################################################################
        {
            'slug': 'empleo',
            'old': None,
            'parent': None,
            'title': 'Empleo',
            'descr': '',
        }, {
            'slug': 'administrativo',
            'old': 'ea',
            'parent': 'empleo',
            'title': 'Administrativo',
            'descr': 'Ofertas de trabajo area administrativo.',
        }, {
            'slug': 'compra-venta',
            'old': 'eb',
            'parent': 'empleo',
            'title': 'Compra y Venta',
            'descr': ('Ofertas de trabajo del area de compra y venta de '
                      'productos y servicios.'),
        }, {
            'slug': 'finanzas-contabilidad',
            'old': 'ec',
            'parent': 'empleo',
            'title': 'Finanzas y Contabilidad',
            'descr': ('Buscas un contador o tienes vacantes en el area de '
                      'contabilidad, entonces publica tu oferta de empleo '
                      'aquí sin costo.'),
        }, {
            'slug': 'atención-al-cliente',
            'old': 'ed',
            'parent': 'empleo',
            'title': 'Atención al Cliente',
            'descr': ('Empleos de atención al cliente, incluyendo en bares y '
                      'restaurantes.'),
        }, {
            'slug': 'technico',
            'old': 'ef',
            'parent': 'empleo',
            'title': 'Téchnico',
            'descr': ('Empleos del area técnico, construcción, electricidad, '
                      'coches, y otros.'),
        }, {
            'slug': 'ingenieria',
            'old': 'eg',
            'parent': 'empleo',
            'title': 'Ingeniería',
            'descr': ('Ofertas de trabajo para personas graduados en un '
                      'area de ingeniería.'),
        }, {
            'slug': 'diseno-y-creativo',
            'old': 'eh',
            'parent': 'empleo',
            'title': 'Diseño y Creativo',
            'descr': ('Ofertas de empleo para personas creativos, escritores, '
                      'diseñadores, grupos de música, y otros.'),
        }, {
            'slug': 'turismo',
            'old': 'ei',
            'parent': 'empleo',
            'title': 'Turismo',
            'descr': ('Ofertas de trabajo en cualquier ramo del area '
                      'turístico.'),
        }, {
            'slug': 'publicidad-y-mercadotecnia',
            'old': 'ek',
            'parent': 'empleo',
            'title': 'Publicidad y Mercadotécnia',
            'descr': ('Empleos del area de la mercadotecnia y todo '
                      'relacionado a la publicidad.'),
        }, {
            'slug': 'educacion',
            'old': 'el',
            'parent': 'empleo',
            'title': 'Educación',
            'descr': ('Ofteras de empleo para profesores de tiempo parcial y '
                      'completo, profesores de idiomas, y otros.'),
        }, {
            'slug': 'medicina-y-sociales',
            'old': 'em',
            'parent': 'empleo',
            'title': 'Medicina y Sociales',
            'descr': ('Empleos de area médico, enfermería y social.'),
        }, {
            'slug': 'otros-empleos',
            'old': 'en',
            'parent': 'empleo',
            'title': 'Otros empleos',
            'descr': ('Cualquier otra oferta de empleo que no queda en '
                      'ninguna de las areas arriba mencionadas.'),
        }, {
            'slug': 'solicitudes-de-empleo',
            'old': 'eo',
            'parent': 'empleo',
            'title': 'Solicitudes de Empleo',
            'descr': ('Si estás buscando trabajo, puedes publicar aquí tu '
                      'solicitud y un breve resumen de tu C.V. Recuerda: '
                      'NO datos personales!'),
        },
        ###############################################################################
        {
            'slug': 'vivienda',
            'old': None,
            'parent': None,
            'title': 'Vivienda',
            'descr': (''),
        }, {
            'slug': 'vender-comprar-casa',
            'old': 'ca',
            'parent': 'vivienda',
            'title': 'Venta y compra de casas',
            'descr': ('Si quieres vender tu casa o estas buscando comprar '
                      'una casa, publica aquí tu anuncio.'),
        }, {
            'slug': 'vender-comprar-departamento',
            'old': 'cb',
            'parent': 'vivienda',
            'title': 'Venta y compra de departamentos',
            'descr': ('Si quieres cender o comprar un departamento, publica '
                      'tu anuncio gratis aquí.'),
        }, {
            'slug': 'rentar-casa',
            'old': 'cc',
            'parent': 'vivienda',
            'title': 'Renta de casas',
            'descr': ('Publica aquí anuncios para la renta de casas.'),
        }, {
            'slug': 'rentar-departamento',
            'old': 'cd',
            'parent': 'vivienda',
            'title': 'Renta de departamentos',
            'descr': ('Si tienes o buscas un departamento para rentar, aquí '
                      'puedes publicar tu anuncio.'),
        }, {
            'slug': 'local-comercial-oficina',
            'old': 'ce',
            'parent': 'vivienda',
            'title': 'Locales Comerciales y Oficinas',
            'descr': ('Renta o venta de locales comerciales y espacios de '
                      'oficina.'),
        }, {
            'slug': 'para-estudiantes',
            'old': 'cf',
            'parent': 'vivienda',
            'title': 'Para Estudiantes',
            'descr': ('Renta de departamentos o habitaciones para '
                      'estudiantes.'),
        },
        ###############################################################################
        {
            'slug': 'vender-y-comprar',
            'old': None,
            'parent': None,
            'title': 'Vender y Comprar',
            'descr': '',
        }, {
            'slug': 'coches-y-camionetas',
            'old': 'va',
            'parent': 'vender-y-comprar',
            'title': 'Coches y Camionetas',
            'descr': ('Anuncios de venta y compra de coches, camionetas, '
                      'motos, bicicletas, y mas.'),
        }, {
            'slug': 'computadoras',
            'old': 'vb',
            'parent': 'vender-y-comprar',
            'title': 'Computadoras',
            'descr': ('Comprar y vender computadoras, laptop, accesorios como '
                      'impresoras, escaner, teclado, vocinas, y mas.'),
        }, {
            'slug': 'electronicos',
            'old': 'vc',
            'parent': 'vender-y-comprar',
            'title': 'Electrónicos',
            'descr': ('Comprar y vender televosores, radios, tocadores de '
                      'discos compactos, y mas.'),
        }, {
            'slug': 'electrodomesticos',
            'old': 'vd',
            'parent': 'vender-y-comprar',
            'title': 'Electrodomésticos',
            'descr': ('Comprar y vender refris, lavadoras, lavatrastes, y '
                      'otros electrodomésticos.'),
        }, {
            'slug': 'celulares-y-contratos',
            'old': 've',
            'parent': 'vender-y-comprar',
            'title': 'Celulares y Contratos',
            'descr': ('Comprar y vender celulares y accesorios para celular. '
                      'También contratos y tarjetas para celular.'),
        }, {
            'slug': 'muebles',
            'old': 'vf',
            'parent': 'vender-y-comprar',
            'title': 'Muebles',
            'descr': ('Comprar y vender muebles, sillas, sillones, armarios, '
                      'mesas y mas.'),
        }, {
            'slug': 'deportes',
            'old': 'vg',
            'parent': 'vender-y-comprar',
            'title': 'Deportes',
            'descr': ('Venta y compra de accesorios y aparatos para '
                      'deportes.'),
        }, {
            'slug': 'Ropa',
            'old': 'vh',
            'parent': 'vender-y-comprar',
            'title': 'Ropa',
            'descr': ('Comprar y vender ropa y accesorios.'),
        }, {
            'slug': 'coleccionables',
            'old': 'vi',
            'parent': 'vender-y-comprar',
            'title': 'Coleccionables',
            'descr': ('Comprar, vender e intercambiar cualquier cosas '
                      'coleccionable.'),
        }, {
            'slug': 'otras',
            'old': 'vk',
            'parent': 'vender-y-comprar',
            'title': 'Otras compras y ventas',
            'descr': ('Venta y compra de otras cosas que no caben en una '
                      'de las categorías mencionadas.'),
        }, {
            'slug': 'gratis',
            'old': 'vl',
            'parent': 'vender-y-comprar',
            'title': 'Gratis',
            'descr': ('Ofrece o busca cosas gratis. Regala lo que ya no '
                      'utilizas.'),
        },
        ###############################################################################
        {
            'slug': 'servicios',
            'old': None,
            'parent': None,
            'title': 'Servicios',
            'descr': '',
        }, {
            'slug': 'hogar',
            'old': 'sa',
            'parent': 'servicios',
            'title': 'Hogar',
            'descr': ('Ofrece o busca servicios de jardinero, sirvienta, '
                      'cocinero y otros.'),
        }, {
            'slug': 'traducciones',
            'old': 'sb',
            'parent': 'servicios',
            'title': 'Traducciones',
            'descr': ('Ofrece o busca servicios de traducción de textos al '
                      'Español, o del Español a otro idioma.'),
        }, {
            'slug': 'mudanzas',
            'old': 'sc',
            'parent': 'servicios',
            'title': 'Mudanzas',
            'descr': ('Encunetra u ofrece servicios de mudanza.'),
        }, {
            'slug': 'internet-y-computadoras',
            'old': 'sd',
            'parent': 'servicios',
            'title': 'Internet y Computadoras',
            'descr': ('Encuentra u ofrece servicios de conección a Internet, '
                      'Café de Internet, o reparación de computadoras.'),
        }, {
            'slug': 'otros-servicios',
            'old': 'se',
            'parent': 'servicios',
            'title': 'Otros Servicios',
            'descr': ('Ofertas para otros servicios.'),
        },
        ###############################################################################
        {
            'slug': 'clases-y-talleres',
            'old': None,
            'parent': None,
            'title': 'Clases y Talleres',
            'descr': '',
        }, {
            'slug': 'idiomas',
            'old': 'ta',
            'parent': 'clases-y-talleres',
            'title': 'Idiomas',
            'descr': ('Talleres y clases para aprender idiomas como el '
                      'Inglés, Francés, Alemán, Japonés, y otros.'),
        }, {
            'slug': 'computacion',
            'old': 'tb',
            'parent': 'clases-y-talleres',
            'title': 'Computación',
            'descr': 'Escuelas y cursos de computación.',
        }, {
            'slug': 'teatro-y-danza',
            'old': 'tc',
            'parent': 'clases-y-talleres',
            'title': 'Teatro y Danza',
            'descr': 'Talleres de danza o teatro.',
        }, {
            'slug': 'literatura-y-pintura',
            'old': 'td',
            'parent': 'clases-y-talleres',
            'title': 'Literatura y Pintura',
            'descr': 'Cursos sobre pintura, literatura, y arte en general.',
        }, {
            'slug': 'otras-classes',
            'old': 'te',
            'parent': 'clases-y-talleres',
            'title': 'Otras classes',
            'descr': 'Otros talleres, cursos y clases.',
        }
    ]
