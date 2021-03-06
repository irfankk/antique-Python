# Generated by Django 3.1.7 on 2021-03-20 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0002_auto_20210320_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Open - currently active'), (1, 'Submitted - has been ordered at the checkout')], default=0, verbose_name='status')),
                ('date_submitted', models.DateTimeField(blank=True, null=True, verbose_name='Date submitted')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Basket',
                'verbose_name_plural': 'Baskets',
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('price', models.DecimalField(decimal_places=3, max_digits=15, null=True, verbose_name='Price')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='cart.basket', verbose_name='Basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='catalogue.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Basket line',
                'verbose_name_plural': 'Basket lines',
            },
        ),
    ]
