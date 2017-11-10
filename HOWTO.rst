=================
acrisel.github.io
=================

references
==========

1. http://nafiulis.me/making-a-static-blog-with-pelican.html
#. https://github.com/getpelican/pelican/wiki/Tips-n-Tricks
#. http://mathamy.com/migrating-to-github-pages-using-pelican.html
#. https://github.com/getpelican/pelican-plugins/tree/master/pelican_comment_system

Prep
====

github
------
create two projects:

1. username/username.github.io-src
#. username/username.github.io

virtualenv
----------

with virtualenvwrapper:

.. code-block:: python

    mkvirtualenv blog
    pip install beautifulsoup4 ghp-import Markdown pelican pysvg shovel

Project folders
---------------

mkdir -p /var/acrisel/sand/blog/
cd /var/acrisel/sand/blog/
git clone https://github.com/Acrisel/acrisel.github.io-src.git blog
cd blog
git clone --recursive https://github.com/getpelican/pelican-themes themes
git clone --recursive https://github.com/getpelican/pelican-plugins plugins
mkdir extra


pelican
-------

pelican-quickstart
~~~~~~~~~~~~~~~~~~

run *pelican-quickstart*

.. code-block::

    Where do you want to create your new web site? [.]
    What will be the title of this web site? > username
    Who will be the author of this web site? > username
    What will be the default language of this web site? [en]
    Do you want to specify a URL prefix? e.g., http://example.com (Y/n) > y
    What is your URL prefix? (see above example; no trailing slash) > http://username.github.io
    Do you want to enable article pagination? (Y/n) > y
    How many articles per page do you want? [10]
    Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) > y
    Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) > y

    None: Here just answer **Y** to *github*

Update pelicanconf.py
~~~~~~~~~~~~~~~~~~~~~

Edit **pelicanconfig.py** to fix *LINKS*

.. code-block:: python

    RELATIVE_URLS = True
    GITHUB_URL = 'https://github.com/username/username.github.io'

    THEME = 'themes/bootstrap2'
    OUTPUT_PATH = 'output'
    PATH = 'content'
    PLUGIN_PATHS = ["plugins",]

    PLUGINS = [
        #'better_figures_and_images',
        'extract_toc','summary','optimize_images','related_posts','sitemap','tipue_search', 'pelican_comment_system'
           ]

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

    STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
    EXTRA_PATH_METADATA = {
        'extra/robots.txt': {'path': 'robots.txt'},
        'extra/favicon.ico': {'path': 'favicon.ico'}
    }
    
    # Custom Home page
    DIRECT_TEMPLATES = (('index', 'blog', 'tags', 'categories', 'archives'))
    PAGINATED_DIRECT_TEMPLATES = (('blog',))
    TEMPLATE_PAGES = {'home.html': 'index.html',}

    # code blocks with line numbers
    PYGMENTS_RST_OPTIONS = {'linenos': 'table'}
    PELICAN_COMMENT_SYSTEM = True
    PELICAN_COMMENT_SYSTEM_IDENTICON_DATA = ('author', 'email')
    
Pelican Comment System
======================

Additional notes regading Pelican Comment System (see document on reference link above)

.. code-block:: python

    mkdir -p [yourtheme]/templates/pcs
    mkdir -p [yourtheme]/static/js
    cp plugins/pelican_commnet_system/theme/templates/pcs/comments.html [yourtheme]/templates/pcs/comments.html
    cp plugins/pelican_commnet_system/theme/static/js/comments.js [yourtheme]/static/js/comments.html
    
Edit comments.js and comments.html to your liking.

Add {{ pcs.comments_quickstart("emailuser", "example.com") }} to article.html below {{ article.content }} 

Create Post
===========

python3 entry.py --post "Title of Article"

Test
====

make html && make devserver
browser: http://localhost:8000/
make stopserver

publish
=======

make publish
make github

Other commands
==============
git push origin master
ghp-import output
git push [-f] git@github.com:Acrisel/acrisel.github.io.git  gh-pages:master
