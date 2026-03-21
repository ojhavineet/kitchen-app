import streamlit as st
import random

st.set_page_config(page_title="Punekar Kitchen", page_icon="🍳")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF4B4B; color: white; font-weight: bold; }
    .recipe-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; margin-bottom: 20px; }
    .shopping-box { background-color: #fff4e6; padding: 15px; border-radius: 10px; border: 1px dashed #ff922b; }
    </style>
    """, unsafe_allow_value=True)

st.title("🍳 Punekar Kitchen")
st.write("Manage your pantry and get meal ideas instantly.")

# --- 1. The Digital Pantry & Automated Shopping List ---
inventory = {
    "Onions / Garlic": True,
    "Tomatoes": True,
    "Paneer / Tofu": False,
    "Rice": True,
    "Atta / Bhakri Flour": False,
    "Mixed Veg (Carrot/Beans)": False,
    "Noodles / Pasta": False,
    "Cheese / Butter / Cream": False,
    "Kanda Lasun / Goda Masala": True,
    "Chinese Sauces": False
}

with st.expander("🛒 Inventory Check (Tick what you HAVE)", expanded=True):
    updated_inventory = {}
    col1, col2 = st.columns(2)
    
    # Create checkboxes and track what is missing
    keys = list(inventory.keys())
    for i, item in enumerate(keys):
        column = col1 if i < 5 else col2
        updated_inventory[item] = column.checkbox(item, value=inventory[item])

# Identify missing items for the shopping list
missing_items = [item for item, involved in updated_inventory.items() if not involved]

# --- 2. Enhanced Recipe Database ---
recipes = {
    "Maharashtrian": [
        {"name": "Kanda Batata Pohe", "needs": ["Onions / Garlic"], "steps": "1. Soak pohe. 2. Sauté onions, chilies, curry leaves. 3. Add turmeric/salt. 4. Mix pohe and steam."},
        {"name": "Zunka Bhakri", "needs": ["Onions / Garlic", "Atta / Bhakri Flour", "Kanda Lasun / Goda Masala"], "steps": "1. Sauté garlic/onions. 2. Add Masala and water. 3. Stir in Besan until thick. 4. Serve with hot Bhakri."}
    ],
    "Indian": [
        {"name": "Paneer Butter Masala", "needs": ["Paneer / Tofu", "Tomatoes", "Cheese / Butter / Cream"], "steps": "1. Puree tomatoes. 2. Cook in butter with spices. 3. Add paneer cubes and cream. 4. Garnish with kasuri methi."},
        {"name": "Veg Pulao", "needs": ["Rice", "Mixed Veg (Carrot/Beans)", "Onions / Garlic"], "steps": "1. Sauté whole spices/onions. 2. Add veggies and washed rice. 3. Add water (2:1 ratio). 4. Pressure cook for 2 whistles."}
    ],
    "Chinese": [
        {"name": "Veg Hakka Noodles", "needs": ["Noodles / Pasta", "Mixed Veg (Carrot/Beans)", "Chinese Sauces"], "steps": "1. Boil noodles. 2. Shred veggies. 3. Stir fry on high heat with sauces. 4. Toss in noodles and pepper."},
        {"name": "Chilli Paneer", "needs": ["Paneer / Tofu", "Chinese Sauces", "Onions / Garlic"], "steps": "1. Dice paneer. 2. Sauté capsicum/onions. 3. Add sauces and paneer. 4. Toss until coated."}
    ],
    "Continental": [
        {"name": "Cheesy Pasta", "needs": ["Noodles / Pasta", "Cheese / Butter / Cream"], "steps": "1. Boil pasta. 2. Make butter-garlic-cheese sauce. 3. Add oregano/flakes. 4. Toss pasta and serve."}
    ]
}

# --- 3. Interaction Logic ---
st.divider()
cuisine = st.radio("What's the mood?", ["Maharashtrian", "Indian", "Chinese", "Continental"], horizontal=True)

if st.button(f"Give me a {cuisine} suggestion"):
    # Check if we have the ingredients for each recipe in that cuisine
    available = []
    for r in recipes[cuisine]:
        if all(updated_inventory[ing] for ing in r["needs"]):
            available.append(r)
    
    if available:
        pick = random.choice(available)
        st.success(f"Suggesting: **{pick['name']}**")
        st.markdown(f"""<div class="recipe-box"><strong>How to make:</strong><br>{pick['steps']}</div>""", unsafe_allow_value=True)
    else:
        st.warning(f"You don't have enough ingredients for a full {cuisine} meal right now. Check your shopping list below!")

# --- 4. The Shopping List (Sticky at the bottom) ---
if missing_items:
    st.divider()
    st.subheader("📝 Smart Shopping List")
    st.write("You are currently out of these items:")
    
    shop_list_html = "".join([f"<li>{item}</li>" for item in missing_items])
    st.markdown(f"""
    <div class="shopping-box">
        <ul>{shop_list_html}</ul>
    </div>
    """, unsafe_allow_value=True)
