# Generated by Django 3.1.3 on 2020-11-23 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
    ]
