import re


def parse_ingredients(user_input: str) -> list:
    """
    Convert messy ingredient input into a clean ingredient list.
    """

    # convert to lowercase
    user_input = user_input.lower()

    # split using comma OR spaces
    ingredients = re.split(r"[,\s]+", user_input)

    # remove empty values
    ingredients = [ingredient.strip() for ingredient in ingredients if ingredient]

    # remove duplicates
    ingredients = list(set(ingredients))

    return ingredients