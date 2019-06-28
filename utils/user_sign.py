import hashlib
from django.conf import settings

def md5(user_id):
    md5_sign=hashlib.md5(settings.SECRET_KEY.encode('utf8'))
    md5_sign.update(bytes(user_id))
    return md5_sign.hexdigest()