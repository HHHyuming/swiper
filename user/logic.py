import os
import requests

from django.conf import settings

from swiper import config
from utils.keys import AVATAR_PATH
from worker import celery_app


@celery_app.task
def send_shortmsg(phone_num, code):
    base_url = 'https://open.ucpaas.com/ol/sms/sendsms'
    data = config.YZX_PARAMS.copy()
    data['param'] = str(code)
    data['mobile'] = phone_num
    response = requests.post(url=base_url, json=data)
    response_json = response.json()
    if response_json['code'] == '000000':
        return 1
    return


@celery_app.task
def save_img(avatar, user):
    filename = os.path.join(settings.MEDIA_ROOT, AVATAR_PATH % user.id)
    with open(filename, 'wb+')as f:
        for chunk in avatar.chunks():
            f.write(chunk)
    return filename
