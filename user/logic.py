import requests

from swiper import config


def send_shortmsg(phone_num, code):
    base_url = 'https://open.ucpaas.com/ol/sms/sendsms'
    data = config.YZX_PARAMS.copy()
    data['param'] = str(code)
    data['mobile'] = phone_num
    response = requests.post(url=base_url, json=data)
    response_json = response.json()
    if response_json['code'] == '000000':
        return 1
