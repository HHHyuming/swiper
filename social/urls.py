from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from social.views import FriendAPIView, SocialAPIView
from user.views import *

router = SimpleRouter()
router.register('social', SocialAPIView)
router.register('friend',FriendAPIView)
urlpatterns = [

]
urlpatterns += router.urls
