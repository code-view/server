REDIS_OPTIONS = {'db': 0}
TEST_REDIS_OPTIONS = {'db': 0}
DEBUG = False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'aiohttp.access': {
            'handlers': ['default'],
            'level': 'INFO',
        },
        'aiohttp.server': {
            'handlers': ['default'],
            'level': 'INFO',
        },
    }
}
