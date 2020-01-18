from rest_framework import serializers

from currencies.models import Currency, ExchangeReferenceRate


class ECBRSSChannelSerializer(serializers.Serializer):
    title = serializers.CharField()


class ECBRSSItemStatisticsExchangeRateSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=5)


class ECBRSSItemStatisticsSerializer(serializers.Serializer):
    exchangeRate = ECBRSSItemStatisticsExchangeRateSerializer()


class ECBRSSItemSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    statistics = ECBRSSItemStatisticsSerializer()


class ECBRSSSerializer(serializers.Serializer):
    channel = ECBRSSChannelSerializer()
    items = ECBRSSItemSerializer(many=True)

    def create(self, validated_data):
        name = validated_data['channel']['title'].split('| ')[1].split(' (')[0]
        iso_code = validated_data['channel']['title'].split('(')[1].split(')')[0]
        currency, created = Currency.objects.get_or_create(name=name, iso_code=iso_code)
        last_scraped = currency.latest_rate_date
        for item in validated_data['items']:
            if item['date'].date() > last_scraped:
                ExchangeReferenceRate.objects.create(currency=currency, date=item['date'], rate=item['statistics']['exchangeRate']['value'])
        return Currency
