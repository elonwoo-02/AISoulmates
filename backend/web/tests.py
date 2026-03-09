from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from web.models.character import Character
from web.models.friend import Friend
from web.models.user import UserProfile
from web.views.utils.ai_config import resolve_ai_config


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


class AISettingsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="config-user", password="pass123")
        self.profile = UserProfile.objects.create(user=self.user)

    def test_get_ai_settings_requires_login(self):
        resp = self.client.get("/api/user/settings/ai/")
        self.assertEqual(resp.status_code, 401)

    def test_get_ai_settings_returns_empty_state(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get("/api/user/settings/ai/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["result"], "success")
        self.assertFalse(resp.data["api_key_configured"])
        self.assertEqual(resp.data["api_key_masked"], "")
        self.assertEqual(resp.data["api_base"], "")
        self.assertTrue(resp.data["using_default_api_key"])
        self.assertTrue(resp.data["using_default_api_base"])

    def test_post_ai_settings_persists_and_masks_key(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            "/api/user/settings/ai/",
            {"api_key": "sk-test-12345678", "api_base": "https://example.com/v1"},
        )
        self.assertEqual(resp.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.api_key, "sk-test-12345678")
        self.assertEqual(self.profile.api_base, "https://example.com/v1")
        self.assertTrue(resp.data["api_key_configured"])
        self.assertTrue(resp.data["api_key_masked"].endswith("5678"))
        self.assertEqual(resp.data["api_base"], "https://example.com/v1")
        self.assertFalse(resp.data["using_default_api_key"])
        self.assertFalse(resp.data["using_default_api_base"])

    def test_post_ai_settings_can_clear_values(self):
        self.profile.api_key = "sk-existing"
        self.profile.api_base = "https://example.com/v1"
        self.profile.save()
        self.client.force_authenticate(user=self.user)

        resp = self.client.post(
            "/api/user/settings/ai/",
            {"api_key": "", "api_base": ""},
        )
        self.assertEqual(resp.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.api_key, "")
        self.assertEqual(self.profile.api_base, "")
        self.assertTrue(resp.data["using_default_api_key"])
        self.assertTrue(resp.data["using_default_api_base"])


class AIConfigResolutionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="resolver", password="pass123")
        self.profile = UserProfile.objects.create(user=self.user)

    @patch.dict("os.environ", {"API_KEY": "env-key", "API_BASE": "https://env.example/v1"}, clear=False)
    def test_resolve_ai_config_prefers_user_values(self):
        self.profile.api_key = "user-key"
        self.profile.api_base = "https://user.example/v1"
        self.profile.save()

        config = resolve_ai_config(self.profile)
        self.assertEqual(config["api_key"], "user-key")
        self.assertEqual(config["api_base"], "https://user.example/v1")
        self.assertFalse(config["using_default_api_key"])
        self.assertFalse(config["using_default_api_base"])

    @patch.dict("os.environ", {"API_KEY": "env-key", "API_BASE": "https://env.example/v1"}, clear=False)
    def test_resolve_ai_config_falls_back_to_environment(self):
        config = resolve_ai_config(self.profile)
        self.assertEqual(config["api_key"], "env-key")
        self.assertEqual(config["api_base"], "https://env.example/v1")
        self.assertTrue(config["using_default_api_key"])
        self.assertTrue(config["using_default_api_base"])

    @patch.dict("os.environ", {"API_KEY": "", "API_BASE": ""}, clear=False)
    def test_resolve_ai_config_raises_when_missing_everywhere(self):
        with self.assertRaisesMessage(ValueError, "API key is not configured"):
            resolve_ai_config(self.profile)


class UserProfileAutoCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="legacy-user", password="pass123")

    def test_login_creates_missing_user_profile(self):
        resp = self.client.post(
            "/api/user/account/login/",
            {"username": "legacy-user", "password": "pass123"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["result"], "success")
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
