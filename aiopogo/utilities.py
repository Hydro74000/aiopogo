from time import time
from json import JSONEncoder
from struct import pack, unpack

from aiohttp import BasicAuth
try:
    from aiosocks import Socks4Auth, Socks5Auth
except ImportError as e:
    class Socks4Auth(Exception):
        def __init__(*args, **kwargs):
            raise ImportError(
                'You must install aiosocks to use a SOCKS proxy.')
    Socks5Auth = Socks4Auth


def f2i(float_val):
    return unpack('<q', pack('<d', float_val))[0]


def to_camel_case(string):
    return ''.join(word.capitalize() for word in string.split('_'))


# JSON Encoder to handle bytes
class JSONByteEncoder(JSONEncoder):
    def default(self, o):
        return o.decode('ascii')


def get_time_ms():
    return int(time() * 1000)

class IdGenerator:
    '''Lehmer random number generator'''
    M = 0x7fffffff  # 2^31 - 1 (A large prime number)
    A = 16807       # Prime root of M

    def __init__(self, seed=1):
        self.seed = seed
        self.request = 1

    def next(self):
        self.seed = (self.seed * self.A) % self.M
        return self.seed

    def request_id(self):
        self.request += 1
        return (self.next() << 32) | self.request


def get_proxy_auth(proxy):
    if proxy.user:
        scheme = proxy.scheme
        if scheme == 'http':
            return BasicAuth(proxy.user, proxy.password)
        elif scheme == 'socks5':
            return Socks5Auth(proxy.user, proxy.password)
        elif scheme == 'socks4':
            return Socks4Auth(proxy.user)
        else:
            raise ValueError(
                'Proxy protocol must be http, socks5, or socks4.')
