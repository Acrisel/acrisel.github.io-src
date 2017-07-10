import sys
from datetime import datetime
import sys
import tempfile
from subprocess import call
import os
import fnmatch
import re


TEMPLATE = """
:title: {title}
:slug: {slug}
:date: {year}-{month}-{day} {hour}:{minute:02d}
:athuors: {authors}
:tags: {tags}
:category: {category}
:summary: {summery}
:status: {status}

"""

BASEDIR=os.getcwd()
INPUTDIR=os.path.join(BASEDIR, 'content')
OUTPUTDIR=os.path.join(BASEDIR, 'output')
PAGESDIR=os.path.join(INPUTDIR, 'pages')
POSTDIR=os.path.join(INPUTDIR, 'posts')

non_alnum=re.compile(r'\W')
multi_dash=re.compile(r'-+')

def find(name, path):
    ''' find first match'''
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return ''

def find_all(name, path):
    ''' find all matchs '''
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def find_pattern(pattern, path):
    ''' find pattern '''
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def create_slug(title):
    result=non_alnum.sub('-', title)
    result=multi_dash.sub('-', result)
    result=result.lower()
    return result

def make_entry(**kws):
    today=datetime.today()
    title=kws['title']
    slug=create_slug(title)
    ext=kws['ext']
    if not ext: ext='rst'

    if kws['page']: location=PAGESDIR
    elif kws['post']: location=POSTDIR
    location=os.path.join(location, str(today.year), "{:0>2}".format(today.month))
    filename="%s.%s" % (slug, ext)

    file_found=find(filename, INPUTDIR)

    filepath=os.path.join(location, filename)

    if file_found:
        if kws['create']:
            raise Exception('File already exist; use edit: %s' % file_found)
        initialize=False
    else: # not found
        if kws['edit']:
            raise Exception('File not found; use create: %s' % filename)
        initialize=True

    if initialize:
        header== TEMPLATE.strip().format(title=title,
                                year=today.year,
                                month=today.month,
                                day=today.day,
                                hour=today.hour,
                                minute=today.minute,
                                slug=slug,
                                authors=','.join(kws['authors']))
        with open(filepath, 'w') as w:
            w.write(t)
        print("File created -> " + filepath)
    else:
        print("File found -> " + filepath)

    if not kws['noedit']:
        EDITOR=kws['editor']
        if not EDITOR:
            EDITOR=os.environ.get('EDITOR','vim')
        call([EDITOR, filepath])

def cmdargs():
    import argparse

    parser = argparse.ArgumentParser(description="""
Create new entry or edit existing one.
""")
    act_ = parser.add_mutually_exclusive_group(required=False)
    act_.add_argument('--create', action='store_true',
                        help="""Ensures file not exist before creating. If exists and --create not present, edit will be assumed.""")
    act_.add_argument('--edit', action='store_true',
                        help="""Ensures file exists before edtiing.  If not exists and --edit not present, create will be assumed.""")

    parser.add_argument('--editor', metavar='PROGRAM', required=False, type=str,
                        help="""override EDITOR environment variable.""")
    parser.add_argument('--no-edit', dest='noedit', required=False, action='store_true',
                        help="""prevent start of editor""")
    parser.add_argument('--tag', dest='tags', required=False,
                        default=list(), action='append',
                        help="""tag[s] to assign""")
    parser.add_argument('--author', dest='authors', required=False,
                        default=list(), action='append',
                        help="""name[s] of author""")
    parser.add_argument('--category', required=False, type=str, default='',
                        help="""category to assign to the article; empty if not given.""")
    parser.add_argument('--summery', required=False,
                        type=str, default='',
                        help="""summery line; empty if not present.""")
    parser.add_argument('--status', required=False, choices=['draft', 'hidden'],
                        default='draft',
                        help="""status of the article.""")
    parser.add_argument('--ext', required=False, type=str, default='rst',
                        help="""extention to use for creating the file.""")
    type_ = parser.add_mutually_exclusive_group(required=True)
    type_.add_argument('--post', action='store_true',
                        help="""set to work on Post type content""")
    type_.add_argument('--page', action='store_true',
                        help="""set to work on Page type content""")

    parser.add_argument('title', type=str, help="""rmask""")
    args = parser.parse_args()
    argsd=vars(args)
    return argsd

if __name__ == '__main__':
    args=cmdargs()
    make_entry(**args)
