# Generated by Django 4.2.4 on 2023-08-31 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
