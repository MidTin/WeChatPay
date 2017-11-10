import requests

from .exceptions import RequestPaymentFail, RequestQueryFail
from .parameters import OrderCreateParameters, OrderQueryParameters, required
from .sign import Signature
from .utils import xml_to_dict


class BasePay:

    TRADE_TYPE = None
    DEFAULT_SIGN_TYPE = 'md5'
    UNIFIED_ORDER_API_URL = r'https://api.mch.weixin.qq.com/pay/unifiedorder'

    def __init__(self, appid, app_key, mch_id):
        self.appid = appid
        self.mch_id = mch_id
        self.app_key = app_key
        self._signature = Signature(app_key)
        self._creation_parameters_cls = OrderCreateParameters
        self._query_parameters_cls = OrderQueryParameters

    def make_creation_params(self, **kwargs):
        params = self._creation_parameters_cls(
            appid=self.appid, mch_id=self.mch_id, trade_type=self.TRADE_TYPE,
            **kwargs)

        sign_type = kwargs.get('sign_type', self.DEFAULT_SIGN_TYPE)
        signature = self._signature.sign(params.params, sign_type)
        return params.xml(signature)

    def make_query_params(self, **kwargs):
        params = self._query_parameters_cls(
            appid=self.appid, mch_id=self.mch_id, **kwargs)

        sign_type = kwargs.get('sign_type', self.DEFAULT_SIGN_TYPE)
        signature = self._signature.sign(params.params, sign_type)
        return params.xml(signature)

    def pay(self, trade_no, total_fee, client_ip, **kwargs):
        payload = self.make_creation_params(
            out_trade_no=trade_no, total_fee=total_fee,
            spbill_create_ip=client_ip, **kwargs)

        try:
            resp = requests.post(self.UNIFIED_ORDER_API_URL, data=payload)
            if resp.status_code != 200:
                raise RequestPaymentFail(f'{resp.content}')
            return xml_to_dict(resp.content)
        except Exception as ex:
            raise RequestPaymentFail(f'{ex}')

    def query(self, **kwargs):
        payload = self.make_query_params(**kwargs)

        try:
            resp = requests.post(self.UNIFIED_ORDER_API_URL, data=payload)
            if resp.status_code != 200:
                raise RequestQueryFail(f'{resp.content}')
            return xml_to_dict(resp.content)
        except Exception as ex:
            raise RequestQueryFail(f'{ex}')


class JSAPIPay:

    TRADE_TYPE = 'JSAPI'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._creation_parameters_cls.openid = required


class NativePay:

    TRADE_TYPE = 'NATIVE'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._creation_parameters_cls.product_id = required
