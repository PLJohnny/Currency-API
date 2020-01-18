from django.contrib import admin
from django.urls import path, include
import currencies.api.urls as currencies_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(currencies_url))
]
