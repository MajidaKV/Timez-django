# Generated by Django 4.0.6 on 2022-07-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'), ('New', 'New'), ('Completed', 'Completed')], default='New', max_length=20),
        ),
    ]
