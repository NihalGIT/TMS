# Generated by Django 4.1.2 on 2022-10-30 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='dim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dim', models.IntegerField()),
            ],
        ),
    ]
