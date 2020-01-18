# Generated by Django 3.0.2 on 2020-01-18 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('iso_code', models.SlugField(default='', editable=False, max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeReferenceRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('rate', models.DecimalField(decimal_places=4, max_digits=8)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_rates', to='currencies.Currency')),
            ],
        ),
    ]