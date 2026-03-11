import pandas as pd


def load_recipes():
    df = pd.read_csv("data/recipes.csv")

    df["ingredients"] = df["ingredients"].apply(
        lambda x: [i.strip().lower() for i in x.split(",")]
    )

    return df


def match_recipes(user_ingredients):

    df = load_recipes()

    user_set = set(user_ingredients)

    results = []

    for _, row in df.iterrows():

        recipe_name = row["name"]
        recipe_ingredients = set(row["ingredients"])

        matched = user_set & recipe_ingredients
        missing = recipe_ingredients - user_set

        score = len(matched) / len(recipe_ingredients)

        results.append(
            {
                "recipe": recipe_name,
                "match_score": score,
                "matched": list(matched),
                "missing": list(missing),
            }
        )

    results = sorted(results, key=lambda x: x["match_score"], reverse=True)

    # IMPORTANT: filter garbage matches
    results = [r for r in results if r["match_score"] >= 0.35]

    return results