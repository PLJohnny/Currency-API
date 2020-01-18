from rest_framework import serializers

from currencies.models import Currency, ExchangeReferenceRate


class CurrencyHistoricalRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeReferenceRate
        fields = (
            'date',
            'rate'
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        lookup_field = 'iso_code'
        fields = (
            'name',
            'iso_code'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'iso_code'}
        }


class CurrencyDetailSerializer(serializers.ModelSerializer):
    exchange_rates = serializers.SerializerMethodField()

    def get_exchange_rates(self, instance):
        rates = instance.exchange_rates.order_by('-date')[:5]
        return CurrencyHistoricalRatesSerializer(rates, many=True).data

    class Meta:
        model = Currency
        lookup_field = 'iso_code'
        fields = (
            'name',
            'iso_code',
            'exchange_rates'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'iso_code'}
        }
