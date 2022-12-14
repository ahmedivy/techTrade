# Generated by Django 4.1 on 2022-08-12 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_product_alter_bid_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remark',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.product'),
        ),
        migrations.AlterField(
            model_name='remark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
