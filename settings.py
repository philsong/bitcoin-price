TENTACLE_TOKEN_SALT = 'xxxxx'

HAOBTC_HOST = 'http://app.haobtc.com'
HAOBTC_PORT = 80

TENTACLE_APPS = {
    'haobtcnotify': {
        'name': 'haobtcnotify',
        'pass': '1234asdf',
        'masterhost': 'http://localhost:13000',
        'server': 'http://localhost:13001'
    }
}

try:
    from local_settings import *
except ImportError:
    pass
    