# Generated by Django 4.0.6 on 2022-08-01 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed')], default='New', max_length=20),
        ),
    ]
