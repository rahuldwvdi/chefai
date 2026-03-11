import streamlit as st
from services.ingredient_corrector import correct_ingredients
from services.recipe_engine import match_recipes
from services.ai_recipe_generator import generate_recipe

st.set_page_config(page_title="ChefAI", page_icon="💗", layout="centered")

# -----------------------------
# CUSTOM UI STYLE
# -----------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Consolas, monospace;
    background-color:#f4f6fb;
}

/* hero section */

.hero{
    background: linear-gradient(135deg,#6c7bff,#8fa6ff);
    padding:40px;
    border-radius:18px;
    text-align:center;
    color:white;
    margin-bottom:30px;
    animation: fadeIn 1s ease-in;
}

.hero h1{
    font-size:60px;
    margin-bottom:5px;
}

.hero p{
    font-size:18px;
}

/* input */

.stTextInput input{
    border-radius:12px;
    padding:14px;
    font-size:16px;
}

/* buttons */

.stButton button{
    background:#6c7bff;
    color:white;
    border-radius:10px;
    padding:10px 25px;
    font-size:16px;
    transition:0.3s;
}

.stButton button:hover{
    transform:scale(1.05);
    background:#5664e5;
}

/* ingredient chips */

.chip{
display:inline-block;
background:#ffffff;
padding:6px 14px;
border-radius:20px;
margin:5px;
box-shadow:0 2px 6px rgba(0,0,0,0.1);
}

/* recipe card */

.recipe-card{
background:white;
border-radius:18px;
padding:20px;
margin-top:20px;
box-shadow:0px 6px 20px rgba(0,0,0,0.08);
animation:fadeIn 0.6s ease-in;
}

.recipe-card h3{
color:#4c5cff;
}

/* spinner */

.spinner{
text-align:center;
font-size:18px;
color:#555;
}

/* animation */

@keyframes fadeIn{
from{opacity:0; transform:translateY(10px);}
to{opacity:1; transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO SECTION
# -----------------------------

st.markdown("""
<div class="hero">
<h1>ChefAI 💗</h1>
<p>cook something amazing with what you already have</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------

if "ingredients" not in st.session_state:
    st.session_state.ingredients = []

# -----------------------------
# INGREDIENT INPUT
# -----------------------------

with st.form("ingredient_form", clear_on_submit=True):

    ingredient = st.text_input(
        "Add ingredient",
        placeholder="egg, tomato, rice..."
    )

    submitted = st.form_submit_button("Add")

    if submitted and ingredient:

        items = [i.strip().lower() for i in ingredient.split(",")]

        for i in items:
            if i and i not in st.session_state.ingredients:
                st.session_state.ingredients.append(i)

# -----------------------------
# INGREDIENT DISPLAY
# -----------------------------

if st.session_state.ingredients:

    st.write("### Ingredients")

    cols = st.columns(4)

    for idx, ing in enumerate(st.session_state.ingredients):

        with cols[idx % 4]:

            if st.button(f"❌ {ing}", key=ing):
                st.session_state.ingredients.remove(ing)
                st.rerun()

# -----------------------------
# GENERATE BUTTON
# -----------------------------

generate = st.button("Generate Recipes 🍳")

# -----------------------------
# GENERATE RECIPES
# -----------------------------

if generate:

    if not st.session_state.ingredients:
        st.warning("Add some ingredients first!")
        st.stop()

    ingredients = correct_ingredients(st.session_state.ingredients)

    st.write("---")

    st.write("## Recipes you can cook")

    recipes = match_recipes(ingredients)

    if recipes:

        for r in recipes[:3]:

            st.markdown(f"""
            <div class="recipe-card">
            <h3>{r['recipe']}</h3>
            <p><b>You have:</b> {", ".join(r['matched'])}</p>
            <p><b>Missing:</b> {", ".join(r['missing'])}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No strong database matches.")

    # -----------------------------
    # AI RECIPE
    # -----------------------------

    st.write("## ChefAI Special 🤖")

    with st.spinner("Cooking up something special..."):

        ai_recipe = generate_recipe(ingredients)

    st.markdown(f"""
    <div class="recipe-card">
    {ai_recipe}
    </div>
    """, unsafe_allow_html=True)