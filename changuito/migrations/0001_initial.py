# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id',
                 models.AutoField(serialize=False,
                                  verbose_name='ID',
                                  primary_key=True,
                                  auto_created=True)),
                ('creation_date',
                 models.DateTimeField(verbose_name='creation date',
                                      default=django.utils.timezone.now)),
                ('checked_out',
                 models.BooleanField(verbose_name='checked out',
                                     default=False)),
                ('user',
                 models.ForeignKey(
                     blank=True,
                     null=True,
                     to=settings.AUTH_USER_MODEL,
                     on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'carts',
                'verbose_name': 'cart',
                'ordering': ('-creation_date', ),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id',
                 models.AutoField(serialize=False,
                                  verbose_name='ID',
                                  primary_key=True,
                                  auto_created=True)),
                ('quantity',
                 models.DecimalField(decimal_places=3,
                                     verbose_name='quantity',
                                     max_digits=18)),
                ('unit_price',
                 models.DecimalField(decimal_places=2,
                                     verbose_name='unit price',
                                     max_digits=18)),
                ('object_id', models.PositiveIntegerField()),
                ('cart',
                 models.ForeignKey(
                     verbose_name='cart',
                     to='changuito.Cart',
                     on_delete=django.db.models.deletion.CASCADE)),
                ('content_type',
                 models.ForeignKey(
                     to='contenttypes.ContentType',
                     on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'items',
                'verbose_name': 'item',
                'ordering': ('cart', ),
            },
        ),
    ]
