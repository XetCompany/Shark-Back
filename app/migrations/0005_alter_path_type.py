# Generated by Django 5.0.4 on 2024-04-12 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_grouppaths_instant_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='path',
            name='type',
            field=models.CharField(choices=[('automobile', 'Автомобильный'), ('railway', 'Железнодорожный'), ('sea', 'Морской'), ('river', 'Речной'), ('air', 'Воздушный'), ('instant', 'Мгновенный')], default='automobile', max_length=255, verbose_name='Тип прохождения'),
        ),
    ]
