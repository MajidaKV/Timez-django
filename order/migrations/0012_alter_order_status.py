# Generated by Django 4.0.6 on 2022-07-30 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('New', 'New'), ('Completed', 'Completed'), ('Accepted', 'Accepted')], default='New', max_length=20),
        ),
    ]
