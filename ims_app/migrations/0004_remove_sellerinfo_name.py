# Generated by Django 4.2.5 on 2023-09-24 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ims_app', '0003_sellerinfo_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerinfo',
            name='name',
        ),
    ]