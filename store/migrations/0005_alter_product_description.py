# Generated by Django 4.0.6 on 2022-08-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_reviewrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=1500),
        ),
    ]