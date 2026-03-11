import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from services.recipe_engine import match_recipes
from services.ingredient_corrector import correct_ingredients
from services.ai_recipe_generator import generate_recipe


st.set_page_config(
    page_title="ChefAI",
    page_icon="🍳",
    layout="centered"
)

# ----------------------
# HEADER
# ----------------------

st.title("🍳 ChefAI")
st.caption("Cook something with what you already have.")

st.divider()

# ----------------------
# STATE
# ----------------------

if "ingredients" not in st.session_state:
    st.session_state.ingredients = []

# ----------------------
# ADD INGREDIENT
# ----------------------

with st.form("add_ing"):

    ingredient = st.text_input(
        "Add ingredient",
        placeholder="tomato"
    )

    submitted = st.form_submit_button("Add")

    if submitted and ingredient:

        ingredient = ingredient.lower().strip()

        if ingredient not in st.session_state.ingredients:
            st.session_state.ingredients.append(ingredient)

# ----------------------
# INGREDIENT CHIPS
# ----------------------

st.subheader("🥕 Ingredients")

cols = st.columns(4)

for i, ing in enumerate(st.session_state.ingredients):

    with cols[i % 4]:

        if st.button(f"❌ {ing}", key=ing):
            st.session_state.ingredients.remove(ing)
            st.rerun()

# ----------------------
# GENERATE BUTTON
# ----------------------

st.divider()

generate = st.button("🍽 Generate Recipes")

# ----------------------
# GENERATE LOGIC
# ----------------------

if generate:

    if not st.session_state.ingredients:
        st.warning("Add ingredients first.")
        st.stop()

    ingredients = correct_ingredients(st.session_state.ingredients)

    st.divider()

    st.subheader("🍳 Recipe Matches")

    recipes = match_recipes(ingredients)

    if recipes:

        for recipe in recipes[:3]:

            with st.container():

                st.markdown(f"### {recipe['recipe']}")

                st.progress(recipe["match_score"])

                col1, col2 = st.columns(2)

                with col1:
                    st.write("✅ You Have")
                    st.write(", ".join(recipe["matched"]) or "None")

                with col2:
                    if recipe["missing"]:
                        st.write("🛒 Missing")
                        st.write(", ".join(recipe["missing"]))
                    else:
                        st.success("Ready to cook!")

                st.divider()

    else:
        st.info("No strong database matches.")

    # ----------------------
    # AI CHEF
    # ----------------------

    st.subheader("🤖 AI Chef Recipe")

    with st.spinner("ChefAI is thinking..."):

        ai_recipe = generate_recipe(ingredients)

    st.markdown(ai_recipe)