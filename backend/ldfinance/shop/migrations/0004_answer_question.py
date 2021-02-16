# Generated by Django 3.1.5 on 2021-02-05 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_max_per_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.question')),
            ],
        ),
    ]
