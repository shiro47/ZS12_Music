# Generated by Django 4.0.6 on 2022-07-15 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songrequestapp', '0002_alter_song_options_rename_song_video_song_song_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='song_title',
            field=models.TextField(default='No title'),
        ),
    ]