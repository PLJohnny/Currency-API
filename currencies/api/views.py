from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from currencies.api.serializers import CurrencySerializer, CurrencyHistoricalRatesSerializer, CurrencyDetailSerializer
from currencies.models import Currency


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    lookup_field = 'iso_code'

    def get_serializer_class(self):
        if self.action == 'list':
            return CurrencySerializer
        if self.action == 'retrieve':
            return CurrencyDetailSerializer

    @action(detail=True, url_name='historical-rates')
    def historical_rates(self, request, *args, **kwargs):
        currency_rates = self.get_object().exchange_rates.order_by('-date')
        page = self.paginate_queryset(currency_rates)
        if page is not None:
            serializer = CurrencyHistoricalRatesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serialized_currency_rates = CurrencyHistoricalRatesSerializer(currency_rates, many=True)
        return Response(serialized_currency_rates.data)
