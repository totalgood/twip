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
    cd twip
    git checkout v0.1.0

If you don't already have one, sign up to get a twitter user account
(@username): [twitter.com/signup](https://twitter.com/signup)

Once you have a user account, sign into it, then set up a twitter App to get an `API_KEY`:
[apps.twitter.com/app/new](https://apps.twitter.com/app/new)

Copy and paste the *Consumer API Key* and *Consumer API Secret* into the indicated places in the file called `settings_template.py` but don't save it there. Instead save the file as a new file named `settings_secret.py`. This file is `.gitignore`d during pushes. Do a `git status` to make sure you didn't accidentally save your secret KEYs in the template file or misname your `settings_secret.py` file. If you see that any tracked/added files have changes then you need to undo them before you do a commit and push to your fork of twip.

To get ready for the first workshop you'll want to make sure you've checked out v0.1.0:

    git checkout v0.1.0

If you want to skip the first session and move directly to the second session you can checkout `v0.2.0`.  This with have all the code from the first workshop session completed for you.

Credits
-------

-   [Hobson Lane](http://hobsonlane.com/) -- Data Scientist for
    [Talentpair](http://talentpair.com/)
-   [Rob Ludwick](https://www.linkedin.com/in/rludwick) -- Co-Instructor, helped craft the proposal and suggested the tweet optimization application
-   [Jeremy Robin](https://www.linkedin.com/in/jeremyrobin) -- Co-Instructor, helped develop the material
-   [PyScaffold](http://pyscaffold.readthedocs.org/) -- Python package
    setup done right (the one obvious way)
