# Generated by Django 4.1.5 on 2023-02-06 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='payment_ref_id',
            field=models.CharField(default=0, max_length=1000),
        ),
    ]
