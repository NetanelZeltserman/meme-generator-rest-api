from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from app.models import Meme, MemeTemplate
from app.repositories.meme_repository import MemeRepository

class TestMemeRepository(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.templates = self.create_meme_templates(3)
        self.memes = self.create_memes(3)

    def create_meme_templates(self, count):
        return [
            MemeTemplate.objects.create(name=f"Template {i}", image_url=f"http://example.com/template{i}.jpg")
            for i in range(1, count + 1)
        ]

    def create_memes(self, count):
        return [
            Meme.objects.create(
                template=self.templates[i],
                top_text=f"Top {i + 1}",
                bottom_text=f"Bottom {i + 1}",
                created_by=self.user
            )
            for i in range(count)
        ]

    def test_get_random_meme_returns_meme(self):
        meme = MemeRepository.get_random_meme()
        self.assertIsInstance(meme, Meme)
        self.assertIn(meme.template.name, [f"Template {i}" for i in range(1, 4)])

    def test_get_random_meme_with_single_meme(self):
        Meme.objects.all().delete()
        single_meme = self.create_memes(1)[0]
        
        meme = MemeRepository.get_random_meme()
        self.assertEqual(meme, single_meme)

    def test_get_random_meme_raises_exception_when_no_memes(self):
        Meme.objects.all().delete()
        
        with self.assertRaises(ObjectDoesNotExist):
            MemeRepository.get_random_meme()

    def test_get_random_meme_distribution(self):
        iterations = 1000
        meme_counts = {meme.id: 0 for meme in self.memes}
        expected_count = iterations / len(meme_counts)

        for _ in range(iterations):
            meme = MemeRepository.get_random_meme()
            meme_counts[meme.id] += 1

        for count in meme_counts.values():
            self.assertGreater(count, 0)
            # Check if the distribution is roughly equal (within 20% of expected)
            self.assertAlmostEqual(count, expected_count, delta=expected_count * 0.2)