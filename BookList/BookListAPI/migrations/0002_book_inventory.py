# Generated by Django 4.2.3 on 2023-09-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookListAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='inventory',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
