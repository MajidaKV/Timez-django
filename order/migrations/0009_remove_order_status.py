# Generated by Django 4.0.6 on 2022-07-29 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
