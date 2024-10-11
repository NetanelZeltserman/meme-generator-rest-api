from app.tests.utils import create_test_user, create_meme_templates, create_memes
from app.repositories.meme_repository import MemeRepository
from django.db.models import ObjectDoesNotExist
from django.test import TestCase
from app.models import Meme

class TestMemeRepository(TestCase):
    def setUp(self):
        self.user = create_test_user()
        self.templates = create_meme_templates(3)
        self.memes = create_memes(3, self.templates[0], self.user)

    def test_get_random_meme_returns_meme(self):
        meme = MemeRepository.get_random_meme()
        self.assertIsInstance(meme, Meme)
        self.assertIn(meme.template.name, [f"Template {i}" for i in range(1, 4)])

    def test_get_random_meme_with_single_meme(self):
        Meme.objects.all().delete()
        single_meme = create_memes(1, self.templates[0], self.user)[0]
        
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