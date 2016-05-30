# twip

Tweet Impact Predictor

## DESCRIPTION

A natural language processing pipeline for predicting the impact (reach
and popularity) of a tweet. Built as part of the PyCon 2016 Natural
Language Processing tutorial and workshop.

- [cryptic slides](https://totalgood.github.io/twip/)
- [slide source](docs/slides)
- [ipython notebooks](docs/notebooks)
- [virtual box instructions](//github.com/talentpair/puppet-python-nlp-tools)

Don't install the latest version from PyPi if you're working through
the tutorial yourself! Tagged version numbers will correspond to
sections of the tutorial and handout material so you can maintain pace
even if you miss a step along the way. Plus it'll be easier to set up your API keys if you clone the repository.

## GETTING STARTED

Rather than installing this module from the cheese shop, clone it to your laptop.

    git clone git@github.com:totalgood/twip.git
    # optional:
    # mkvirtualenv twip
    pip install -e twip
    cd twip/docs/notebooks
    ipython notebook

That way you can edit the source code. Even better, make your own fork so you can easily issue pull requests. Obviously it needs a lot of help.

## GOT TWEETS?

To use the tweetget app, you also need a Twiter API key.

If you don't already have one, sign up to get a twitter user account like @yournewusername:

[twitter.com/signup](https://twitter.com/signup)

And we'll be happy to be your first followers, just tweet us at:

- Hobson Lane: [@hobsonlane]((https://twitter.com/hobsonlane)
- Jeremy Robin: [@robusican]((https://twitter.com/robustican)
- Dan Fellin: [@eupharis](https://twitter.com/eupharis)

Once you have a user account, sign into it, then create a new twitter app with an `API_KEY`:

[apps.twitter.com/app/new](https://apps.twitter.com/app/new)

Copy and paste the *Consumer API Key* and *Consumer API Secret* into the indicated places in the file called `settings_template.py` but don't save it there. Instead save the file as a new file named `settings_secret.py`. This file is `.gitignore`d during pushes. Do a `git status` to make sure you didn't accidentally save your secret KEYs in the template file or misname your `settings_secret.py` file. If you see that any tracked/added files have changes then you need to undo them before you do a commit and push to your fork of twip.

Alternatively, check out the settings_secret.py file for the environment variables you can set to hold these secret values.

## CREDITS

- [Hobson Lane](//hobsonlane.com/) Data Scientist @ [Talentpair](talentpair.com)  
- [Dan Fellin](//www.linkedin.com/in/dan-fellin-611637b6) Engineer @ [Talentpair](talentpair.com)  
- [Jeremy Robin](//www.linkedin.com/in/jeremyrobin) CTO @ [Talentpair](talentpair.com)  
- [Talentpair](//talentpair.com/)  
- [Rob Ludwick](//www.linkedin.com/in/rludwick): Proposal editting  
- [PyScaffold](//pyscaffold.readthedocs.org/): Python packages done right  
- [gensim](https://radimrehurek.com/gensim/tutorial.html): **The Star of the Show**  
