import hashlib
import hmac

from .utils import encode_string


class Signature:

    def __init__(self, key):
        self.key = key
        self._suffix = f'&key={key}'

    def get_md5(self):
        return hashlib.md5()

    def get_sha256(self):
        return hmac.new(encode_string(self.key), digestmod=hashlib.sha256)

    def sign(self, params: dict, sign_type: str='md5') -> str:
        try:
            hash_ = getattr(self, f'get_{sign_type.lower()}')()
        except AttributeError:
            raise ValueError(f'{sign_type} does not supported')

        sorted_params = sorted(list(params.items()))
        unhash_string = '&'.join(
            [f'{k}={v}' for k, v in sorted_params if v])

        hash_.update(f'{unhash_string}{self._suffix}'.encode())
        return hash_.hexdigest().upper()

    def validate(self, params: dict, sign: str, sign_type: str='md5') -> bool:
        params.pop('sign', None)

        local_sign = self.sign(params, sign_type)
        return local_sign == sign


if __name__ == '__main__':
    s = Signature('192006250b4c09247ec02edce69f6a2d')
    params = dict(
        appid='wxd930ea5d5a258f4f', mch_id='10000100', device_info=1000,
        body='test', nonce_str='ibuaiVcKdpRxkhJA')

    r1 = s.sign(params, 'sha256') == '6A9AE1657590FD6257D693A078E1C3E4BB6BA4DC30B23E0EE2496E54170DACD6'

    r2 = s.sign(params) == '9A0A8659F005D6984697E2CA0A9CF3B7'
    print(r1)
    print(r2)
