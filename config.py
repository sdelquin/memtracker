from prettyconf import config

DATABASE = config('DATABASE', default='memtracker.db')
MAX_DATES = config('MAX_DATES', default='10', cast=config.eval)
USER = config('USER')
PLACE = config('PLACE')
APPS = config('APPS', cast=config.eval)
