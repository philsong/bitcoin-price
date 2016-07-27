import urllib
import re
import requests
from hashlib import md5
from urlparse import urljoin
import settings
import string

TENTACLE_TOKEN_SALT = getattr(settings, 'TENTACLE_TOKEN_SALT', 'ha0btc.b1tc01n$Iwdollar')

def request_tentacle(app, method, path, params=None):
    if params is None:
        params = {}
    appconfig = settings.TENTACLE_APPS[app]
    kw = {'auth': (appconfig['name'], appconfig['pass'])}
    kw['timeout'] = 10
    url = urljoin(appconfig['masterhost'], path)
    # if url.startswith('https://'):
    #     kw['verify'] = defaults.TENTACLE_CA_CERTS
    if method == 'GET':
        body = urllib.urlencode(params)
        if body:
            url = '%s?%s' % (url, body)
        r = requests.get(url, **kw)
    else:
        # POST
        kw['json'] = params
        r = requests.post(url, **kw)
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 400:
        raise APIError(r.status_code, r.json()['error'])
    else:
        raise APIError(r.status_code, r.text)

def push_message(packet, channel=None, sid=None):
    if sid:
        packet['sid'] = sid
    if channel:
        packet['channel'] = channel
    return request_tentacle('haobtcnotify',
                            'POST', '/tentacle/messages/',
                            packet)

def generate_tentacle_session(user_id):
    rand = get_random_string(8)
    rand_md5 = md5('%s-%s' % (rand, TENTACLE_TOKEN_SALT)).hexdigest()
    rand += rand_md5[:2]   # tailing simple checksum
    base = '%s-%s-%s' % (user_id, rand, TENTACLE_TOKEN_SALT)
    digest = md5(base).hexdigest()
    return '%s-%s-%s' % (user_id, rand, digest)

class TentacleSessionError(Exception):
    pass

def recognize_tentacle_session(session):
    arr = session.split('-')
    if len(arr) != 3:
        raise TentacleSessionError('Wrong number of -')

    user_id, rand, digest = arr
    if not re.match('\d+$', user_id):
        raise TentacleSessionError('Wrong first part')

    rand_head, rand_sum = rand[:-2], rand[-2:]
    if md5('%s-%s' % (rand_head, TENTACLE_TOKEN_SALT)).hexdigest()[:2] != rand_sum:
        raise TentacleSessionError('Wrong second part')

    base = '%s-%s-%s' % (user_id, rand, TENTACLE_TOKEN_SALT)
    if md5(base).hexdigest() != digest:
        raise TentacleSessionError('Wrong third part')

    return int(user_id)

def get_random_string(length=12, allowed_chars=string.ascii_letters + string.digits):
    random.seed(hashlib.sha256(("%s%s%s" % (random.getstate(), time.time(),
            "BLAHBLAHBLAH")).encode('utf-8')
        ).digest())
    return ''.join([random.choice(allowed_chars) for i in range(length)])

class APIError(Exception):
    def __init__(self, code, msg, api_code=None):
        self.code = code
        self.api_code = api_code
        super(APIError, self).__init__(msg)

