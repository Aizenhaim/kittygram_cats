from rest_framework import routers

from .views import DestinationViewSet, TravelViewSet

router = routers.DefaultRouter()
router.register('destinations', DestinationViewSet)
router.register('travels', TravelViewSet)

urlpatterns = router.urls
