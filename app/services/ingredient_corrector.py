from rapidfuzz import process

# known ingredients from our recipe dataset
KNOWN_INGREDIENTS = [
    "egg",
    "rice",
    "milk",
    "sugar",
    "butter",
    "onion",
    "soy sauce",
    "tomato",
    "carrot",
    "broccoli",
    "pepper"
]


def correct_ingredients(user_ingredients):

    corrected = []

    for ingredient in user_ingredients:

        match, score, _ = process.extractOne(ingredient, KNOWN_INGREDIENTS)

        if score > 80:
            corrected.append(match)
        else:
            corrected.append(ingredient)

    return corrected