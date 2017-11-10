#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Acrisel Team'
SITENAME = "Acrisel's Community Blog"
SITEURL = 'https://acrisel.github.io'

# can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = True

GITHUB_URL = 'https://github.com/Acrisel/acrisel.github.io'
#GITHUB_URL = 'https://acrisel.github.io'
#DISQUS_SITENAME = "acrisel-community-blog"
REVERSE_CATEGORY_ORDER = True
LOCALE = "C"
DEFAULT_PAGINATION = 4
DEFAULT_DATE = (2017, 8, 9, 14, 1, 1)

# global metadata to all the contents
DEFAULT_METADATA = {'showcomments' : 'yes',}

THEME = 'themes/pelican-bootstrap3'
DOCUTIL_CSS = True
OUTPUT_PATH = 'output'
PATH = 'content'
PLUGIN_PATHS = ["plugins",]
PLUGINS = [
    #'better_figures_and_images',
    'extract_toc',
    'summary',
    'optimize_images',
    'related_posts',
    'sitemap',
    'tipue_search',
    'pelican_comment_system',
    'i18n_subsites',
    'share_post',
    #'image_process',
    'minchin.pelican.plugins.image_process',
           ]

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}
SHOW_DATE_MODIFIED = True

SITEMAP={
    'format':'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5, },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'},
}

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
         ('Acrisel', 'http://www.acrisel.com/'),
         ('Acrisel Open Source', 'http://www.github.com/acrisel'),
         ('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
        )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico',]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}
GOOGLEPLUS = "https://plus.google.com/111013214708506107651??rel=author"
FAVICON = 'favicon.ico'
BOOTSTRAP_THEME = 'cerulean'        # Bootswatch sub-theme for Bootstrap
PYGMENTS_STYLE = 'xcode'        # Syntax highlighting theme

# Custom Home page
DIRECT_TEMPLATES = ['index', 'blog', 'authors', 'search',] # 'tags', 'categories', 'archives',]
PAGINATED_DIRECT_TEMPLATES = ['blog',]
#TEMPLATE_PAGES = { #'home.html': 'index.html',#
#                  'recent.json': 'api/recent.json',}

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

PELICAN_COMMENT_SYSTEM = True
PELICAN_COMMENT_SYSTEM_IDENTICON_DATA = ('author', 'email')

DISPLAY_AUTHORS_ON_SIDEBAR = True

IMAGE_PROCESS = {
    'crisp': {'type': 'responsive-image',
              'srcset': [('1x', ["scale_in 800 600 True"]),
                         ('2x', ["scale_in 1600 1200 True"]),
                         ('4x', ["scale_in 3200 2400 True"]),
                         ],
               'default': '1x',
             },
    'large-photo': {'type': 'responsive-image',
                    'sizes': '(min-width: 1200px) 800px, (min-width: 992px) 650px, \
                              (min-width: 768px) 718px, 100vw',
                    'srcset': [('600w', ["scale_in 600 450 True"]),
                               ('800w', ["scale_in 800 600 True"]),
                               ('1600w', ["scale_in 1600 1200 True"]),
                               ],
                    'default': '800w',
                   },
    }
