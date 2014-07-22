# Generated by Django 2.1.11 on 2019-08-11 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_user_own_rent_house'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='saving',
        ),
        migrations.AddField(
            model_name='user',
            name='have_pet_cover',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ("Don't know", "Don't know")], max_length=50, verbose_name='pet'),
        ),
        migrations.AddField(
            model_name='user',
            name='savings',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='savings'),
        ),
        migrations.AlterField(
            model_name='user',
            name='have_vision_cover',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ("Don't know", "Don't know")], max_length=50, verbose_name='vision'),
        ),
    ]