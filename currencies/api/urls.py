from django.urls import include, path
from rest_framework.routers import DefaultRouter

from currencies.api.views import CurrencyViewSet

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet)

urlpatterns = [
    path('', include(router.urls))
]
