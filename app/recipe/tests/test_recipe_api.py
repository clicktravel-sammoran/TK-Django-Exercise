from core.models import Recipe, Ingredient
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPES_URL = reverse('recipe:recipe-list')


def recipe_url(recipe_id):
    """Return URL for a recipe"""

    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(params={}):
    """Create and return a sample recipe"""

    defaults = {
        'name': 'Spaghetti Carbonara',
        'description': 'A lovely meal',
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


def sample_ingredient(recipe, name='Spaghetti'):
    """Create and return a sample ingredient"""

    return Ingredient.objects.create(recipe=recipe, name=name)


class RecipeApiTests(TestCase):
    """Test Recipe API endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_get_all_recipes(self):
        """GET /recipes/ - Test returning a list of recipes"""

        recipe1 = sample_recipe({
            'name': 'Bangers and Mash',
            'description': 'A hearty meal'
        })

        recipe2 = sample_recipe({
            'name': 'Chips and peas',
            'description': 'A basic meal'
        })

        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('name'), recipe1.name)
        self.assertEqual(response.data[1].get('name'), recipe2.name)

    def test_get_all_recipes_with_name_filter(self):
        sample_recipe()
        recipe = sample_recipe({
            'name': 'A chicken dinner',
            'description': 'A clucking good meal'
        })

        serializer = RecipeSerializer(recipe)

        filter_term = 'chicken'
        response = self.client.get(
            RECIPES_URL,
            {'name': filter_term}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, response.data)

    def test_get_all_recipes_with_name_filter_no_results(self):
        """Test retrieving a list of recipes when filter returns no matches"""

        sample_recipe({
            'name': 'Bangers and Mash',
            'description': 'A hearty meal'
        })

        filter_term = 'Chips'
        response = self.client.get(
            RECIPES_URL,
            {'name': filter_term}
        )

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_recipe_by_id_success(self):
        """Test retrieving a recipe by unique ID"""

        sample_recipe()
        recipe = sample_recipe({
            'name': 'Bangers and Mash',
            'description': 'A hearty meal'
        })
        recipe.ingredients.add(sample_ingredient(recipe=recipe, name='Mash'))

        serializer = RecipeSerializer(recipe)

        url = recipe_url(recipe.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_recipe_by_id_not_found(self):
        """Test retrieving a recipe by ID when the recipe doesn't exist"""

        response = self.client.get(recipe_url(recipe_id=1))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recipe(self):
        """Test creating a new recipe"""

        ingredient_name_1 = 'Sausage'
        ingredient_name_2 = 'Gravy'

        payload = {
            'name': 'Bangers And Mash',
            'description': 'Whack it all together',
            'ingredients': [
                {'name': ingredient_name_1},
                {'name': ingredient_name_2},
            ]
        }

        response = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        number_of_ingredients = \
            Ingredient.objects.filter(recipe__id=response.data["id"]).count()
        self.assertEqual(number_of_ingredients, 2)

    def test_create_recipe_invalid_request(self):
        """Test creating a new recipe with invalid payload"""

        payload = {
            'name': '',
        }

        response = self.client.post(RECIPES_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_recipe(self):
        """Test updating of a recipe"""

        recipe = sample_recipe()

        ingredient1 = sample_ingredient(recipe, name='Garlic')
        ingredient2 = sample_ingredient(recipe, name='Cheese')

        recipe.ingredients.add(ingredient1, ingredient2)

        new_ingredient_name = 'Egg'
        payload = {
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': [
                {'name': new_ingredient_name}
            ]
        }

        response = self.client.patch(
            recipe_url(recipe_id=recipe.id), payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recipe = Recipe.objects.get(id=response.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 1)
        self.assertEqual(new_ingredient_name, ingredients[0].name)

    def test_delete_recipe(self):
        """Test deleting an existing recipe"""

        recipe = sample_recipe()

        response = self.client.delete(recipe_url(recipe_id=recipe.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        all_recipes = Recipe.objects.all()
        self.assertEqual(len(all_recipes), 0)

        all_ingredients = Ingredient.objects.all()
        self.assertEqual(len(all_ingredients), 0)

    def test_delete_non_existing_recipe(self):
        """Test deleting a non existent recipe"""

        response = self.client.delete(recipe_url(recipe_id=1))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
