# Generated by Django 4.0.6 on 2022-08-01 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_order_status_remove_orderproduct_variation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted')], default='New', max_length=20),
        ),
    ]
