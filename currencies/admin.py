from django.contrib import admin

from currencies.models import Currency, ExchangeReferenceRate

admin.site.register(Currency)
admin.site.register(ExchangeReferenceRate)
