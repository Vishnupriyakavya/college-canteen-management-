# Generated by Django 5.1.7 on 2025-03-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='images',
            field=models.ImageField(upload_to='items'),
        ),
    ]
