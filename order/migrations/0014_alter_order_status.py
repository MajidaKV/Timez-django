# Generated by Django 4.0.6 on 2022-07-30 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('New', 'New'), ('Cancelled', 'Cancelled'), ('Accepted', 'Accepted')], default='New', max_length=20),
        ),
    ]
