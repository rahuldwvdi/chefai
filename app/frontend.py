import streamlit as st
from services.ingredient_corrector import correct_ingredients
from services.recipe_engine import match_recipes
from services.ai_recipe_generator import generate_recipe

st.set_page_config(page_title="ChefAI", page_icon="💗", layout="centered")

# -----------------------------
# UI STYLE
# -----------------------------

st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: Consolas, monospace;
    background-color:#f7f7f7;
}

/* title */

.title {
    font-size:64px;
    color:#5a6ff0;
    font-weight:bold;
    text-align:center;
    animation:fadeIn 1.5s ease-in;
}

.subtitle{
    text-align:center;
    font-size:22px;
    margin-bottom:30px;
    color:#333;
}

/* input */

.stTextInput input{
    background:#f5e3a5;
    border-radius:14px;
    padding:16px;
    font-size:18px;
}

/* button */

.stButton button{
    background:#5a6ff0;
    color:white;
    border-radius:10px;
    padding:10px 25px;
    font-size:18px;
    transition:0.3s;
}

.stButton button:hover{
    transform:scale(1.05);
    background:#4254d6;
}

/* recipe cards */

.recipe-card{
    background:white;
    padding:20px;
    border-radius:15px;
    margin-top:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.08);
    animation:fadeIn 0.7s ease-in;
}

/* ingredient chips */

.chip{
    display:inline-block;
    background:#f5e3a5;
    padding:6px 14px;
    border-radius:12px;
    margin:4px;
    font-size:14px;
}

/* floating hearts */

.heart{
  position: fixed;
  bottom: -10px;
  font-size: 20px;
  animation: floatUp 8s infinite;
  color:#ff5c8d;
}

@keyframes floatUp {
  0% {transform: translateY(0); opacity:1;}
  100% {transform: translateY(-900px); opacity:0;}
}

@keyframes fadeIn{
from{opacity:0; transform:translateY(20px);}
to{opacity:1; transform:translateY(0);}
}

</style>

<div class="heart" style="left:10%">💗</div>
<div class="heart" style="left:25%">💗</div>
<div class="heart" style="left:40%">💗</div>
<div class="heart" style="left:60%">💗</div>
<div class="heart" style="left:75%">💗</div>

""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------

st.markdown('<div class="title">chefAI 💕</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">cook something with what you already have &lt;3</div>', unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------

if "ingredients" not in st.session_state:
    st.session_state.ingredients = []

# -----------------------------
# INGREDIENT INPUT
# -----------------------------

ingredient = st.text_input("what you have in your kitchen ?")

if ingredient:

    ingredient = ingredient.lower().strip()

    if ingredient not in st.session_state.ingredients:
        st.session_state.ingredients.append(ingredient)

# -----------------------------
# INGREDIENT CHIPS
# -----------------------------

if st.session_state.ingredients:

    chip_html = ""

    for i in st.session_state.ingredients:
        chip_html += f'<span class="chip">{i}</span>'

    st.markdown(chip_html, unsafe_allow_html=True)

# -----------------------------
# GENERATE BUTTON
# -----------------------------

generate = st.button("generate recipe 🍳")

# -----------------------------
# GENERATE RESULTS
# -----------------------------

if generate:

    ingredients = correct_ingredients(st.session_state.ingredients)

    with st.spinner("chefAI is cooking something cute... 💕"):

        recipes = match_recipes(ingredients)

    # -----------------------------
    # DATABASE RECIPES
    # -----------------------------

    if recipes:

        st.subheader("recipes you can cook")

        for r in recipes[:3]:

            st.markdown(f"""
            <div class="recipe-card">
            <h3>{r['recipe']}</h3>
            <p><b>You have:</b> {", ".join(r['matched'])}</p>
            <p><b>Missing:</b> {", ".join(r['missing'])}</p>
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------
    # AI GENERATED RECIPE
    # -----------------------------

    st.subheader("chefAI special 🤖")

    with st.spinner("thinking..."):

        ai_recipe = generate_recipe(ingredients)

    st.markdown(f"""
    <div class="recipe-card">
    {ai_recipe}
    </div>
    """, unsafe_allow_html=True)