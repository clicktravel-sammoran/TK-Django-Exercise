from core.models import Recipe
from recipe import serializers
from rest_framework import viewsets


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes that exist in the database"""

    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Retrieve recipes with the name filter"""

        name = self.request.query_params.get('name')
        queryset = Recipe.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
