:title: Pelican Post Template Controls
:slug: pelican-post-template-controls
:date: 2017-08-27 17:12:44
:athuors: Arnon Sela
:tags: Python, Pelican, templates, comments

--------------------------------------
How to selectively show comments block
--------------------------------------

Synopsis
========

This post will cover how to control templates from articles. In specific, how to enable or disable comments block in posts.

Motivation
==========

We are using Pelican static website framework with `Pelican Comment System <https://pypi.python.org/pypi/pelican-comment-system>`_. However, we wanted to disable for some of the articles the ability to show comments.

How to
======

There were three elements that needed to control commnets:

1. Add *DEFAULT_METADATA* item named *showcomments* to *pelicanconf.py* :

    .. code-block:: python

        DEFAULT_METADATA = {'showcomments' : 'yes',}

#. Add a condition to show comments block in theme's article.html:

    .. code-block:: python

        {% if article.showcomments == "yes" %}
            {{ pcs.comments_quickstart("support", "acrisel.com") }}
        {% endif %}

#. Add *:showcomments: no* metadata to disable comments block in any article.

    .. code-block:: python

        :date: 2017-07-09 10:20
        :modified: 2017-07-09 18:40
        :category: example
        :slug: pelican-selective-display-content
        :showcomments: no
        :authors: The Acrisel Team
        :summary: pelican selective display content

That's it, done.

Conclusion
==========

We showed here a method to dynamically control the display of comments block.  This method can be used for other content elements. Others metadata tags can be added to bother *DEFAULT_METADATA* and articles.

References
==========

   | `Pelican Comment System <https://pypi.python.org/pypi/pelican-comment-system>`_ by Bernhard Scheirle
