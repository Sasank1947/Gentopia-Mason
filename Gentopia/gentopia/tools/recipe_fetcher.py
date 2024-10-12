import requests
from typing import Optional, Type
from pydantic import BaseModel, Field
from gentopia.tools.basetool import BaseTool

class RecipeFetcherArgs(BaseModel):
    ingredients: str = Field(..., description="Comma-separated list of ingredients")

class RecipeFetcher(BaseTool):
    """Fetches recipes based on ingredients."""
    name = "recipe_fetcher"
    description = "Fetches recipes based on a list of ingredients."
    args_schema: Optional[Type[BaseModel]] = RecipeFetcherArgs

    def _run(self, ingredients: str) -> str:
        """Fetch recipes from Spoonacular API."""
        api_key = "ed1823d3f7224cdda6e28db00bedaedd"  # Replace this with your actual API key
        response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={api_key}")
        
        if response.status_code == 200:
            recipes = response.json()
            return str(recipes)  # Return the recipes as a string
        else:
            return "Error fetching recipes."
