from django.test import TestCase

from currencies.models import Currency


class CurrencyTest(TestCase):
    def setUp(self):
        Currency.objects.create(name='US Dollar', iso_code='USD')
        Currency.objects.create(name='Danish krone', iso_code='DKK')

    def test_currency_name(self):
        usd = Currency.objects.get(iso_code='USD')
        dkk = Currency.objects.get(iso_code='DKK')
        self.assertEqual(
            usd.name, 'US Dollar')
        self.assertEqual(
            dkk.name, 'Danish krone')
