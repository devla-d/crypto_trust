# Generated by Django 3.2.6 on 2022-02-25 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OngoingTrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('sysmbol', models.CharField(max_length=50)),
                ('interval', models.IntegerField(default=0)),
                ('leverage', models.FloatField(default=0)),
                ('pay', models.IntegerField(blank=True, default=30, null=True)),
            ],
        ),
    ]