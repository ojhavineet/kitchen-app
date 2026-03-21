import streamlit as st
import random

st.set_page_config(page_title="Punekar Kitchen", page_icon="🍳")

# --- Custom Styling for Mobile ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF4B4B; color: white; }
    .recipe-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    </style>
    """, unsafe_allow_value=True)

st.title("🍳 Punekar Kitchen")
st.write("Smart suggestions for your daily meals.")

# --- 1. The Digital Pantry ---
with st.expander("🛒 What's in your Kitchen?", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        has_onion = st.checkbox("Onions / Garlic", value=True)
        has_tomato = st.checkbox("Tomatoes", value=True)
        has_paneer = st.checkbox("Paneer / Tofu")
        has_rice = st.checkbox("Rice", value=True)
        has_atta = st.checkbox("Atta / Bhakri Flour")
    with col2:
        has_veggies = st.checkbox("Mixed Veg (Carrot/French Beans)")
        has_noodles = st.checkbox("Noodles / Pasta")
        has_cheese = st.checkbox("Cheese / Butter / Cream")
        has_spices = st.checkbox("Kanda Lasun Masala / Goda Masala", value=True)
        has_sauces = st.checkbox("Chinese Sauces (Soy/Chili)")

# --- 2. Advanced Recipe Database ---
# Each cuisine now has multiple options for the "Refresh" feature
recipes = {
    "Maharashtrian": [
        {
            "name": "Kanda Batata Pohe",
            "needs": [has_onion],
            "steps": "1. Soak pohe for 2 mins. 2. Sauté onions, chilies, and curry leaves in oil. 3. Add turmeric and salt. 4. Mix in pohe and steam for 2 mins with a lid."
        },
        {
            "name": "Zunka Bhakri",
            "needs": [has_onion, has_atta, has_spices],
            "steps": "1. Sauté lots of garlic and onions. 2. Add Kanda Lasun Masala and water. 3. Slowly stir in Besan until thick. 4. Serve with hot Bhakri."
        }
    ],
    "Indian": [
        {
            "name": "Paneer Butter Masala",
            "needs": [has_paneer, has_tomato, has_cheese],
            "steps": "1. Puree tomatoes and ginger. 2. Cook in butter with red chili powder. 3. Add paneer cubes and a splash of cream/milk. 4. Garnish with kasuri methi."
        },
        {
            "name": "Veg Pulao",
            "needs": [has_rice, has_veggies, has_onion],
            "steps": "1. Sauté whole spices and onions. 2. Add chopped veggies and washed rice. 3. Add 2 cups water for 1 cup rice. 4. Pressure cook for 2 whistles."
        }
    ],
    "Chinese": [
        {
            "name": "Veg Hakka Noodles",
            "needs": [has_noodles, has_veggies, has_sauces],
            "steps": "1. Boil noodles al-dente. 2. Shred veggies thinly. 3. Stir fry on high heat with soy sauce and vinegar. 4. Toss in noodles and black pepper."
        },
        {
            "name": "Chilli Paneer (Dry)",
            "needs": [has_paneer, has_sauces, has_onion],
            "steps": "1. Dice paneer and coat in cornflour (optional). 2. Sauté capsicum and onions. 3. Add soy sauce, green chili sauce, and paneer. 4. Toss until coated."
        }
    ],
    "Continental": [
        {
            "name": "Pink Sauce Pasta",
            "needs": [has_noodles, has_tomato, has_cheese],
            "steps": "1. Boil pasta. 2. Make a quick tomato sauce and mix with a bit of cream/cheese. 3. Add oregano and chili flakes. 4. Toss pasta and serve."
        }
    ]
}

# --- 3. The Logic & Refresh Mechanism ---
st.divider()
cuisine = st.radio("Pick your craving:", ["Maharashtrian", "Indian", "Chinese", "Continental"], horizontal=True)

# This button triggers the "Refresh" by picking a random valid recipe
if st.button(f"Suggest a {cuisine} Meal"):
    # Filter recipes based on ingredients available
    available_options = [r for r in recipes[cuisine] if all(r["needs"])]
    
    if available_options:
        pick = random.choice(available_options)
        st.success(f"How about **{pick['name']}**?")
        st.markdown(f"""
        <div class="recipe-box">
        <strong>Method:</strong><br>{pick['steps']}
        </div>
        """, unsafe_allow_value=True)
    else:
        st.warning("Oops! You're missing some key ingredients for this cuisine. Try ticking more items above or switch cuisines.")

st.info("💡 Don't like the result? Just click the button again to 'Refresh' and get a different suggestion!")
