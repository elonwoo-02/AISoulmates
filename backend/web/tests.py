from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from web.models.character import Character
from web.models.friend import Friend
from web.models.user import UserProfile


class HomepageSearchTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_1 = User.objects.create_user(username="alice", password="pass123")
        self.user_2 = User.objects.create_user(username="bob", password="pass123")
        self.profile_1 = UserProfile.objects.create(user=self.user_1)
        self.profile_2 = UserProfile.objects.create(user=self.user_2)

        photo = SimpleUploadedFile("test.jpg", b"filecontent", content_type="image/jpeg")
        self.c1 = Character.objects.create(
            author=self.profile_1,
            name="Ocean Guide",
            profile="A deep sea story",
            photo=photo,
        )
        self.c2 = Character.objects.create(
            author=self.profile_2,
            name="Forest Spirit",
            profile="Mysterious ocean winds",
            photo=SimpleUploadedFile("test2.jpg", b"filecontent2", content_type="image/jpeg"),
        )

    def test_search_matches_multiple_fields(self):
        resp = self.client.get("/api/homepage/index/", {"search_query": "ocean"})
        self.assertEqual(resp.status_code, 200)
        ids = [item["id"] for item in resp.data["characters"]]
        self.assertIn(self.c1.id, ids)
        self.assertIn(self.c2.id, ids)

        resp_by_author = self.client.get("/api/homepage/index/", {"search_query": "alice"})
        self.assertEqual(resp_by_author.status_code, 200)
        ids = [item["id"] for item in resp_by_author.data["characters"]]
        self.assertEqual(ids, [self.c1.id])

    def test_search_uses_term_intersection(self):
        resp = self.client.get("/api/homepage/index/", {"search_query": "ocean spirit"})
        self.assertEqual(resp.status_code, 200)
        ids = [item["id"] for item in resp.data["characters"]]
        self.assertEqual(ids, [self.c2.id])

    def test_invalid_items_count_returns_400(self):
        resp = self.client.get("/api/homepage/index/", {"items_count": "abc"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data["result"], "invalid_items_count")

    def test_negative_items_count_clamped_to_zero(self):
        resp = self.client.get("/api/homepage/index/", {"items_count": -10})
        self.assertEqual(resp.status_code, 200)
        ids = [item["id"] for item in resp.data["characters"]]
        self.assertEqual(ids, [self.c2.id, self.c1.id])


class FriendListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.me = User.objects.create_user(username="me", password="pass123")
        self.author = User.objects.create_user(username="author1", password="pass123")
        self.me_profile = UserProfile.objects.create(user=self.me)
        self.author_profile = UserProfile.objects.create(user=self.author)

        self.character = Character.objects.create(
            author=self.author_profile,
            name="Guide",
            profile="Story",
            photo=SimpleUploadedFile("char.jpg", b"char", content_type="image/jpeg"),
        )
        self.friend = Friend.objects.create(me=self.me_profile, character=self.character)

    def test_get_list_includes_character_photo(self):
        self.client.force_authenticate(user=self.me)
        resp = self.client.get("/api/friend/get_list/", {"items_count": 0})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["result"], "success")
        self.assertEqual(len(resp.data["friends"]), 1)
        character = resp.data["friends"][0]["character"]
        self.assertIn("photo", character)
        self.assertTrue(character["photo"])
