from core import models
from django.test import TestCase


class ModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient string representation"""

        recipe = models.Recipe.objects.create(
            name='Spaghetti Carbonara',
            description='Stick some Spaghetti in a pan and pray',
        )

        ingredient = models.Ingredient.objects.create(
            recipe=recipe,
            name='Spaghetti'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""

        recipe = models.Recipe.objects.create(
            name='Spaghetti Carbonara',
            description='Stick some Spaghetti in a pan and pray',
        )

        self.assertEqual(str(recipe), recipe.name)
