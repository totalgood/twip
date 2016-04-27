import os


def get_env_setting(setting):
    """ Get the environment setting or return exception
    """
    rv = os.environ.get(setting, None)
    if rv:
        return rv
    else:
        error_msg = "%s env variable not found, set them in your bashrc" % setting
        raise Exception(error_msg)


TWITTER_API_KEY = get_env_setting('TWITTER_API_KEY')
TWITTER_API_SECRET = get_env_setting('TWITTER_API_SECRET')

MERGED_DATA_LOCATION = 'data.json'
OLDEST_ID_PATH = 'raw/oldest_id.txt'

RATE_LIMIT = 180
RATE_LIMIT_WINDOW = 900
