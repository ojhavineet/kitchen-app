import streamlit as st

# 1. App Configuration for Mobile
st.set_page_config(page_title="Kitchen Companion", layout="centered")

st.title("🍳 Kitchen Companion")
st.subheader("What's for dinner tonight?")

# 2. The Digital Pantry (Editable Inventory)
with st.expander("📝 Update Your Ingredients", expanded=True):
    st.write("Tick what you have in the kitchen:")
    
    col1, col2 = st.columns(2)
    with col1:
        has_onion = st.checkbox("Onions / Garlic", value=True)
        has_tomato = st.checkbox("Tomatoes", value=True)
        has_paneer = st.checkbox("Paneer / Tofu")
        has_rice = st.checkbox("Rice", value=True)
        has_atta = st.checkbox("Atta (Flour)")
    
    with col2:
        has_veggies = st.checkbox("Mixed Veggies (Carrot/Beans)")
        has_noodles = st.checkbox("Noodles / Pasta")
        has_cheese = st.checkbox("Cheese / Butter")
        has_ginger = st.checkbox("Ginger / Chili")
        has_sauces = st.checkbox("Soy Sauce / Vinegar")

# 3. The Recipe Database (Logic)
def get_suggestions():
    suggestions = {"Indian": "Simple Dal & Rice", "Chinese": "Veg Stir Fry", "Continental": "Salad"}
    
    # Indian Logic
    if has_paneer and has_tomato:
        suggestions["Indian"] = "Paneer Butter Masala"
    elif has_atta and has_onion:
        suggestions["Indian"] = "Onion Paratha"
    elif has_rice and has_veggies:
        suggestions["Indian"] = "Veg Pulao"

    # Chinese Logic
    if has_noodles and has_veggies and has_sauces:
        suggestions["Chinese"] = "Veg Hakka Noodles"
    elif has_paneer and has_sauces:
        suggestions["Chinese"] = "Chilli Paneer"
    elif has_rice and has_sauces:
        suggestions["Chinese"] = "Fried Rice"

    # Continental Logic
    if has_noodles and has_cheese:
        suggestions["Continental"] = "Cheesy White Sauce Pasta"
    elif has_veggies and has_cheese:
        suggestions["Continental"] = "Baked Vegetables"
    elif has_atta and has_tomato and has_cheese:
        suggestions["Continental"] = "Homemade Thin Crust Pizza"
        
    return suggestions

# 4. Displaying Suggestions
st.divider()
st.write("### Choose a Cuisine:")
tab1, tab2, tab3 = st.tabs(["🇮🇳 Indian", "🇨🇳 Chinese", "🇪🇺 Continental"])

recs = get_suggestions()

with tab1:
    st.info(f"Today's Indian Suggestion: **{recs['Indian']}**")
    if st.button("Get Recipe Steps (Indian)"):
        st.write("1. Sauté onions and ginger. 2. Add spices. 3. Cook main ingredient. 4. Serve hot!")

with tab2:
    st.info(f"Today's Chinese Suggestion: **{recs['Chinese']}**")
    if st.button("Get Recipe Steps (Chinese)"):
        st.write("1. High flame toss veggies. 2. Add soy sauce. 3. Mix in base. 4. Garnish & Serve.")

with tab3:
    st.info(f"Today's Continental Suggestion: **{recs['Continental']}**")
    if st.button("Get Recipe Steps (Conti)"):
        st.write("1. Boil water for base. 2. Make butter-garlic sauce. 3. Add cheese. 4. Toss & Serve.")
