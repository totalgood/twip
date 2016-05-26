#!/usr/bin/python
"""Build slides for PyCon Tutorial using `pandoc`

requires pandoc binary command-line app:

    sudo apt-get install -y pandoc

>>> build_pycon

"""
import os
import subprocess
from traceback import print_exc
from pug.nlp.util import mkdir_p

from twip.constant import DOCS_PATH
BLOG_PATH = os.path.abspath(os.path.join(DOCS_PATH, '..', 'hobson.github.io', 'images'))
POSTS_PATH = os.path.join(BLOG_PATH, '_posts')
SLIDES_PATH = os.path.join(DOCS_PATH, 'slides')

mkdir_p(os.path.join(DOCS_PATH, 'images'))
mkdir_p(os.path.join(SLIDES_PATH))


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Build html reveal.js slides from markdown in docs/ dir")
    parser.add_argument(
        '-v',
        '--verbose',
        help='Whether to show progress messages on stdout, including HTML',
        action='store_true')
    parser.add_argument(
        '--version',
        help='print twip package version and exit.',
        action='version',
        version='twip {ver}'.format(ver=__version__))
    parser.add_argument(
        '-b',
        '--blog_path',
        help='Path to source markdown files. Must contain an `images` subdir',
        default=BLOG_PATH)
    parser.add_argument(
        '-s',
        '--slide_path',
        help='Path to dir for output slides (HTML). An images subdir will be added. A slides subdir should already exist.',
        default=DOCS_PATH)
    parser.add_argument(
        '-p',
        '--presentation',
        help='Source markdown base file name (without .md extension). The HTML slides will share the same basename.',
        default='2015-10-27-Hacking-Oregon-Hidden-Political-Connections')
    return parser.parse_args(args)


def run(args=None):
    cmd = """cp -f "{}/"*.md "{}" """.format(SLIDES_PATH, POSTS_PATH)
    output = subprocess.check_output(cmd.split())
    cmd = """rsync -avzf "{}/images/" "{}/images" """.format(BLOG_PATH, DOCS_PATH)
    output = subprocess.check_output(cmd.split())

    markdown_file = "{}/{}.md".format(POSTS_PATH, args.presentation)
    html_file = "{}/{}.html".format(DOCS_PATH, args.presentation)

    cmd = """pandoc -t revealjs --mathjax --template={}/pandoc-template-for-revealjs.html -V theme=moon -s "$MARKDOWN" -o "$HTML" """.format(
        SLIDES_PATH, markdown_file, html_file)
    output = subprocess.check_output(cmd.split())
    cmd = r'''sed -i -e 's/src\=\"\/images/src="\/talks\/images/g' ''' + '"{}"'.format(html_file)


def update_git_repo():
    """Because GitPython sucks (cmd.commit() hangs)

    # pip install GitPython
    # import git
    # repo = git.Repo('.')
    # g = git.cmd.Git('.')
    # g.pull()
    # g.push()
    # g.commit()

    """
    today
    commands = """
        git add docs/*.html
        git add docs/images/
        git add docs*.ipynb
        git commit -am "autocommit new docs build {}"
        git push hobson
        git push origin

        git checkout master
        git merge gh-pages -m "automerge gh-pages into master"
        git push hobson
        git push origin

        git checkout gh-pages
        git merge master -m "automerge master into gh-pages"
        git push hobson
        git push origin
        """.format(datetime.datetime.today().isoformat())

    for cmd in commands.split('\n'):
        cmd = cmd.strip()
        if cmd:
            try:
                output = subprocess.check_output(cmd.split())
                print(output)
            except CalledProcessError:
                print_exc()
