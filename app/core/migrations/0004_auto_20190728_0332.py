# Generated by Django 2.1.10 on 2019-07-28 03:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(150)], verbose_name='age'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='registered'),
        ),
        migrations.AddField(
            model_name='user',
            name='education',
            field=models.CharField(blank=True, choices=[('High school', 'High school'), ('College', 'College'), ('University', 'University')], max_length=50, null=True, verbose_name='education'),
        ),
        migrations.AddField(
            model_name='user',
            name='employment',
            field=models.CharField(blank=True, choices=[('Student', 'Student'), ('Full time', 'Full time'), ('Part time', 'Part time')], max_length=50, null=True, verbose_name='employment'),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='user',
            name='income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator], verbose_name='income'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, null=True, unique=True, verbose_name='phone number'),
        ),
        migrations.AddField(
            model_name='user',
            name='zipcode',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(5)], verbose_name='zipcode'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
    ]