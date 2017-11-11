import copy
import inspect
from xml.etree import ElementTree as ET

from .exceptions import MissingRequiredParam
from .utils import random_str


class required:
    pass


class Parameters:

    appid = required
    mch_id = required
    out_trade_no = required
    sign = required
    nonce_str = required

    def __init__(self, **kwargs):
        kwargs['nonce_str'] = random_str()

        self.params = {}
        for name in dir(self):
            attr = getattr(self, name, None)
            if name.startswith('__') or inspect.ismethod(attr):
                continue

            if name != 'sign' and attr == required and not kwargs.get(name):
                raise MissingRequiredParam(
                    f'Value of {name} is required.')

            self.params[name] = kwargs.get(name)

    def xml(self, signature):
        params = copy.deepcopy(self.params)
        params['sign'] = signature

        root = ET.Element('xml')
        for key, value in params.items():
            if value is None:
                continue

            if getattr(self, key) != required:
                value = f'<![CDATA[{value}]]>'

            el = ET.SubElement(root, str(key))
            el.text = str(value)

        return ET.tostring(root, encoding='utf-8')


class OrderCreateParameters(Parameters):

    body = required
    total_fee = required
    spbill_create_ip = required
    notify_url = required
    trade_type = required

    sign_type = 'MD5'
    fee_type = 'CNY'

    device_info = None
    detail = None
    attach = None
    time_start = None
    time_end = None
    goods_tag = None
    product_id = None
    limit_pay = None
    openid = None
    scene_info = None


class OrderQueryParameters(Parameters):

    out_trade_no = None

    def __init__(self, **kwargs):
        if not kwargs.get('out_trade_no') and kwargs.get('transaction_id'):
            raise MissingRequiredParam(
                'Missing out_trade_no and transaction_id, must provided one of them.')

        super().__init__(**kwargs)
