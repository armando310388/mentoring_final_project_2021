# Generated by Django 3.2.4 on 2021-10-02 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_web', models.CharField(max_length=100)),
                ('creation_time', models.DateTimeField()),
                ('url', models.CharField(max_length=400)),
                ('clicks_counter', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
