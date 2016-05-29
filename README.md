twip
====

Tweet Impact Predictor

Description
-----------

A natural language processing pipeline for predicting the impact (reach
and popularity) of a tweet. Built as part of the PyCon 2016 Natural
Language Processing tutorial and workshop. For more information see the
[tutorial repository](https://github.com/totalgood/pycon-2016-nlp-tutorial).

Don't install the latest version from PyPi if you're working through
the tutorial yourself! Tagged version numbers will correspond to
sections of the tutorial and handout material so you can maintain pace
even if you miss a step along the way. Plus it'll be easier to set up your API keys if you clone the repository.

GETTING STARTED
---------------

Rather than installing this module from the cheese shop, fork the repository on GitHub and then clone it to your laptop (replacing `totalgood` with your account name:

    git clone git@github.com:totalgood/twip.git
    # optional:
    # mkvirtualenv twip
    pip install -r requirements.txt
    cd twip/docs/notebooks
    ipython notebook

If you don't already have one, sign up to get a twitter user account
(@username): [twitter.com/signup](https://twitter.com/signup)

Once you have a user account, sign into it, then set up a twitter App to get an `API_KEY`:
[apps.twitter.com/app/new](https://apps.twitter.com/app/new)

Copy and paste the *Consumer API Key* and *Consumer API Secret* into the indicated places in the file called `settings_template.py` but don't save it there. Instead save the file as a new file named `settings_secret.py`. This file is `.gitignore`d during pushes. Do a `git status` to make sure you didn't accidentally save your secret KEYs in the template file or misname your `settings_secret.py` file. If you see that any tracked/added files have changes then you need to undo them before you do a commit and push to your fork of twip.

Credits
-------

-   [Hobson Lane](//hobsonlane.com/) -- Data Scientist for
-   [Dan Fellin](//www.linkedin.com/in/dan-fellin-611637b6): Co-Instructor, helped develop the material
-   [Jeremy Robin](//www.linkedin.com/in/jeremyrobin): -- Co-Instructor, helped develop the material
-   [Talentpair](//talentpair.com/)
-   [Rob Ludwick](//www.linkedin.com/in/rludwick): proposal editting
-   [PyScaffold](//pyscaffold.readthedocs.org/): Python package setup done right