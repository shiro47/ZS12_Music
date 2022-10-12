from django.test import TestCase
from songrequestapp.models import song, songs_play_history, songs_blacklist
from django.utils import timezone
from django.urls import reverse

class songrequestapp_test(TestCase):
    
    def test_index_view(self):
        url = reverse("songrequestapp:index")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
