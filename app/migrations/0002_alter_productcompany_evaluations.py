# Generated by Django 5.0.4 on 2024-04-10 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcompany',
            name='evaluations',
            field=models.ManyToManyField(blank=True, to='app.evaluationandcomment', verbose_name='Оценки и комментарии'),
        ),
    ]