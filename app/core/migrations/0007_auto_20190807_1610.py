# Generated by Django 2.1.10 on 2019-08-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190805_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='content_digital',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='content_income',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='content_liability',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='content_medical',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='content_overall',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='content_stuff',
            field=models.TextField(blank=True, null=True),
        ),
    ]
