# Generated by Django 3.0.2 on 2020-02-10 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_profile_is_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]