# Generated by Django 4.1.1 on 2022-09-17 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_id'),
        ('authuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favourite',
            field=models.ManyToManyField(blank=True, to='post.post'),
        ),
    ]
