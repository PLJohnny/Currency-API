from rest_framework import serializers

from currencies.models import Currency, ExchangeReferenceRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class CurrencyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class CurrencyHistoricalRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeReferenceRate
        fields = '__all__'
