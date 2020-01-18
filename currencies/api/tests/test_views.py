from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from currencies.api.serializers import CurrencySerializer, CurrencyHistoricalRatesSerializer, CurrencyDetailSerializer
from currencies.models import Currency

client = Client()


class GetAllCurrenciesTest(TestCase):
    def setUp(self):
        Currency.objects.create(name='US Dollar', iso_code='USD')
        Currency.objects.create(name='Danish krone', iso_code='DKK')
        Currency.objects.create(name='Pound sterling', iso_code='GBP')
        Currency.objects.create(name='Czech koruna', iso_code='CZK')

    def test_get_all_currencies(self):
        response = client.get(reverse('currency-list'))
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        self.assertEqual(response.data.get("results"), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCurrencyTest(TestCase):
    def setUp(self):
        self.usd = Currency.objects.create(name='US Dollar', iso_code='USD')

    def test_get_existing_single_currency(self):
        response = client.get(
            reverse('currency-detail', kwargs={'iso_code': self.usd.iso_code}))
        usd = Currency.objects.get(pk=self.usd.pk)
        serializer = CurrencyDetailSerializer(usd)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistant_single_currency(self):
        response = client.get(
            reverse('currency-detail', kwargs={'iso_code': 'ABC'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSingleCurrencyHistoricalRatesTest(TestCase):
    def setUp(self):
        self.usd = Currency.objects.create(name='US Dollar', iso_code='USD')

    def test_get_existing_single_currency_historical_rates(self):
        response = client.get(
            reverse('currency-historical-rates', kwargs={'iso_code': self.usd.iso_code}))
        usd_rates = Currency.objects.get(pk=self.usd.pk).exchange_rates.all()
        serializer = CurrencyHistoricalRatesSerializer(usd_rates, many=True)
        self.assertEqual(response.data.get("results"), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistant_single_currency_historical_rates(self):
        response = client.get(
            reverse('currency-historical-rates', kwargs={'iso_code': 'ABC'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
