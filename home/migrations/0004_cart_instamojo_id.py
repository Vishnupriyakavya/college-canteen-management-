# Generated by Django 5.1.7 on 2025-03-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_cart_user_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='instamojo_id',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
