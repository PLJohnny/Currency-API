from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=255)
    iso_code = models.SlugField(max_length=3, db_index=True, editable=False, default='')

    def __str__(self):
        return self.iso_code

    class Meta:
        verbose_name_plural = 'Currencies'


class ExchangeReferenceRate(models.Model):
    currency = models.ForeignKey(Currency, related_name='exchange_rates', on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.DecimalField(max_digits=8, decimal_places=4)

    def __str__(self):
        return f'{self.currency}: {self.date} - {self.rate}'
