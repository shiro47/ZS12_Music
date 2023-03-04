from django.test import TestCase
from songrequestapp.models import song, songs_play_history, songs_blacklist
from django.utils import timezone

# models test
class Song_Model_Test(TestCase):

    def create_song(self, song_url="only a test", song_title="yes, this is only a test", song_duration="test", song_thumbnail="test"):
        return song.objects.create(song_url=song_url, song_title=song_title, song_duration=song_duration, song_thumbnail=song_thumbnail)

    def test_song_creation(self):
        w = self.create_song()
        self.assertTrue(isinstance(w, song))
        
class Songs_play_history_Test(TestCase):
    
    def create_song_play_history(self, song_url="only a test", song_title="yes, this is only a test", song_duration="test", song_thumbnail="test"):
        return song.objects.create(song_url=song_url, song_title=song_title, song_duration=song_duration, song_thumbnail=song_thumbnail)

    def test_song_play_history_creation(self):
        w = self.create_song()
        self.assertTrue(isinstance(w, song))

class Songs_blacklist_Test(TestCase):
    
    def create_song_blacklist(self, song_url="only a test", song_title="yes, this is only a test", song_duration="test", song_thumbnail="test"):
        return song.objects.create(song_url=song_url, song_title=song_title, song_duration=song_duration, song_thumbnail=song_thumbnail)

    def test_song_blacklist_creation(self):
        w = self.create_song()
        self.assertTrue(isinstance(w, song))
