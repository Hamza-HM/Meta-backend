# Generated by Django 4.2.5 on 2023-09-29 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookListAPI', '0002_book_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('inventory', models.IntegerField()),
            ],
            options={
                'indexes': [models.Index(fields=['price'], name='BookListAPI_price_2b059c_idx')],
            },
        ),
    ]
