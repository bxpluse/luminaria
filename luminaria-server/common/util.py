import random
import string

import bcrypt
from tldextract import extract


def parse_word(word):
    # word = word.strip()
    # word = re.sub('[^A-Za-z0-9]+', '', word)
    # word = re.sub(r'^\W+', '', word)
    strp_chars = ' ~!@#$%^&*()_+-=[]{};:<>,./?|\n'
    word = word.strip(strp_chars)
    return word


def str_to_float(num: str):
    return float("{:.4f}".format(float(num)))


def float_to_float(num: float):
    return float("{:.4f}".format(num))


def type_transform(val, data_type):
    if data_type == 'int':
        val = int(val)
    elif data_type == 'float':
        val = float(val)
    elif data_type == 'bool':
        if val.upper() in {'TRUE', '1'}:
            val = True
        else:
            val = False
    elif data_type == 'list':
        val = eval(val)
    return val


def gen_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def extract_domain(url):
    tsd, domain, tsu = extract(url)
    return domain


def hash_pw(password):
    password = password.encode('ascii')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed
