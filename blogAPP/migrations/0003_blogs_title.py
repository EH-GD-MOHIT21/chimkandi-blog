# Generated by Django 3.2.5 on 2021-07-23 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogAPP', '0002_auto_20210724_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='title',
            field=models.CharField(default='Admin Provided Blog', max_length=150),
        ),
    ]
