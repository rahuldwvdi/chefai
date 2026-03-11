from dotenv import load_dotenv
load_dotenv()
from services.ingredient_parser import parse_ingredients
from services.recipe_engine import match_recipes
from services.ingredient_corrector import correct_ingredients
from services.ai_recipe_generator import generate_recipe

def main():

    print("\nWelcome to ChefAI")
    print("Your AI-powered kitchen assistant\n")

    user_input = input("Enter ingredients you have: ")

    ingredients = parse_ingredients(user_input)
    ingredients = correct_ingredients(ingredients)

    print("\nClean Ingredients List:")
    print(ingredients)

    recipes = match_recipes(ingredients)

    print("\nBest Recipe Suggestions:\n")

    for recipe in recipes[:3]:

        print("Recipe:", recipe["recipe"])
        print("Match Score:", round(recipe["match_score"], 2))
        print("You Have:", recipe["matched"])
        if recipe["missing"]:
            print("Missing:", recipe["missing"])
        else:
            print("Missing: None — you can cook this now!")
        print()
    best_score = recipes[0]["match_score"]

    if best_score < 0.5:
        print("\nNo strong recipe match found.")
        print("\nGenerating AI recipe...\n")

        ai_recipe = generate_recipe(ingredients)

        print(ai_recipe)


if __name__ == "__main__":
    main()