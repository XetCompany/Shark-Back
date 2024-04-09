# Generated by Django 5.0.4 on 2024-04-09 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_productcompany_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouppaths',
            name='warehouse',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.pointincity', verbose_name='Склад'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='decline_reason',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Причина отклонения'),
        ),
    ]