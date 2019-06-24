from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from user.views import *

router = SimpleRouter()
router.register('user', UserApiView)
urlpatterns = [

]
urlpatterns += router.urls
