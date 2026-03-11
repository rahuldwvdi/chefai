from groq import Groq
import streamlit as st
import os

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def generate_recipe(ingredients):

    ingredient_text = ", ".join(ingredients)

    prompt = f"""
You are ChefAI.

The user ONLY has these ingredients:

{ingredient_text}

STRICT RULES:
- You MUST only use these ingredients
- You may add ONLY salt, oil, pepper, spices
- Do NOT introduce other food ingredients

Return the recipe in this format:

Recipe Name:

Ingredients Used:

Cooking Steps:
1.
2.
3.

Estimated Calories:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content