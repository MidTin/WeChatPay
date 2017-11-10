import random
import string
from xml.etree import ElementTree as ET


def encode_string(s: str):
    if isinstance(s, str):
        return s.encode()
    return s


def random_str(length=32):
    return ''.join(
        random.choices(f'{string.ascii_letters}{string.digits}', k=length))


def xml_to_dict(value):
    root = ET.fromstring(value)
    ret = {}
    for el in root.iter():
        if el.tag == 'xml':
            continue

        ret[el.tag] = el.text

    return ret
