from base64 import b64encode
from hashlib import pbkdf2_hmac
from os import urandom

__LOWER = 'abcdefghijklmnopqrstuvwxyz'
__UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
__DIGITS = '0123456789'
__SPECIAL = ';~,`@!%$$&^?*#:"/|(){}[]<>\'\\'

def b64(inp):
    "base64 endcode a bytes array"
    return b64encode(inp).decode('ascii').replace('/', '_')

def random_salt(size=19):
    "generate a random salt string of a given size"
    return b64(urandom(2*size))[:size]


def hash_password(password, salt=None, iterations=354703, salt_size=19,
                  hash_name='sha512'):
    """hash a password to a hashed string that can be safely stored
    and then later used with `test_password()` to test whether a
    provided password matches the stored one.

    Arguments:
    -----------
     password   str, password to store, required
     salt       str or None, salt to use        [None, generated]
     iterations int, number of iterations                [354703]
     salt_size  int, size (in bytest) of auto-generated salt [19]
     hash_name  str, name of hash algoritm ofo pbkdf2_hmac [sha512]

    Returns
    ---------
      string, strictly ASCII encoded that can be safely saved and later
              used with `test_password()` to test a candidate password.

    Notes
    -------
    the resulting string should be a strong hash that can be stored to
    disk without high risk of brute-force attack.  By default, it uses a
    randomly generated 19-character salt, minimizing the likliehood of
    existing rainbow tables.  The hashing uses `pbdkf2_hmac()` with
    'sha512' and the generated salt and a large number (default 354703)
    of iterations to deliberately slow down computation time.
    This function should take at least 100 ms to run.
    """
    if salt is None:
        salt = random_salt(size=salt_size)
    pwhash = b64(pbkdf2_hmac(hash_name, password.encode('ascii'),
                             salt.encode('ascii'), iterations))
    return '&'.join([hash_name, f'{iterations:d}', salt, pwhash])

def test_password(password, pwhash):
    """test whether password matches a hash, as set with `hash_password()`"""
    thash, shash = 'a', 'b'
    if isinstance(pwhash, bytes):
        pwhash = pwhash.decode('ascii')
    if isinstance(pwhash, str) and pwhash.count('&') == 3:
        hash_name, niter, salt, shash = pwhash.split('&')
        thash = hash_password(password, salt=salt,
                              iterations=int(niter),
                              hash_name=hash_name)
    return len(thash)> 100 and (thash == shash)


def check_password_rules(pwtest, minlen=8, lowercase=1, uppercase=1,
                         digits=1, special=1, invalid=''):
    """check password rules for minimum lenghth, number of lower, upper case letters,
       digits, special characters and avoiding invalid characters

    Arguments:
    -----------
     pwtest     str, password to test, required
     minlen     int, minimum length                       [8]
     lowercase  int, minimum number of lower case letters [1]
     uppercase  int, minimum number of upper case letters [1]
     digiits    int, minimum number of digits             [1]
     special    int, minimum number of special characters [1]
     invalid    str, string containing invalid special characters  ['']

    Returns
    ---------
    (valid, reasons) where `valid` is True for a test password that
                    satisfies the rules, and `reasons` is tuple of
                     strings with reasons for failure.

    Notes
    ------
    1. the default special characters include
    ;~,`@!%$$&^?*#:"/|(){}[]<>\'

    """
    reasons = []
    if len(pwtest) < minlen:
        reasons.append(f'must be at least {minlen} characters')
    lc, uc, di, sp = 0, 0, 0, 0
    if invalid is None:
       invalid = ''
    _special = ''.join([s for s in __SPECIAL if s not in invalid])

    for x in pwtest:
        if x in __LOWER:
            lc += 1
        elif x in __UPPER:
            uc += 1
        elif x in __DIGITS:
            di += 1
        elif x in _special:
            sp += 1
        if x in invalid:
            reasons.append(f"cannont contain characters in '{x}'.")

    if lc < lowercase:
        reasons.append(f'must contain at least {lowercase} lower case letters.')
    if uc < uppercase:
        reasons.append(f'must contain at least {uppercase} upper case letters.')
    if sp < special:
        reasons.append(f'must contain at least {special} special characters: {_special}')
    if di < digits:
         reasons.append(f'must contain at least {digits} digits.')

    return len(reasons)==0, tuple(reasons)
