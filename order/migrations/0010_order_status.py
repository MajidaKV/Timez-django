# Generated by Django 4.0.6 on 2022-07-29 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_remove_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted'), ('Completed', 'Completed')], default='New', max_length=20),
        ),
    ]