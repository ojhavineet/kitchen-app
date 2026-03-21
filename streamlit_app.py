import streamlit as st
import random

st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="🌶️")

# --- Styling ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; }
    .recipe-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. The Database (Massive Expansion) ---
# In a real app, this would be a separate file with 1000s of rows
MASTER_INGREDIENTS = [
    "Onions", "Tomatoes", "Ginger", "Garlic", "Green Chilies", "Coriander", "Curry Leaves",
    "Paneer", "Potato", "Cauliflower", "Spinach", "Green Peas", "Capsicum", "Carrot", "French Beans",
    "Atta", "Rice", "Poha", "Besan", "Maida", "Rava", "Jowar Flour", "Bajra Flour",
    "Tur Dal", "Moong Dal", "Chana Dal", "Urad Dal", "Masoor Dal", "Matki",
    "Noodles", "Pasta", "Soy Sauce", "Vinegar", "Chili Sauce", "Schezwan Sauce",
    "Cheese", "Butter", "Fresh Cream", "Milk", "Curd",
    "Kanda Lasun Masala", "Goda Masala", "Turmeric", "Cumin Seeds", "Mustard Seeds", "Hing"
]

recipes = [
    {"name": "Misal Pav", "cuisine": "Maharashtrian", "needs": ["Matki", "Onions", "Kanda Lasun Masala"], "steps": "1. Sprout and boil matki. 2. Make a spicy 'kat' using onions, coconut, and masala. 3. Serve with pav, farsan, and lemon."},
    {"name": "Pithla Bhakri", "cuisine": "Maharashtrian", "needs": ["Besan", "Onions", "Garlic", "Jowar Flour"], "steps": "1. Make a thin batter of besan. 2. Sauté onions and garlic. 3. Add batter and stir until thick. 4. Serve with hot Jowar Bhakri."},
    {"name": "Gobi Manchurian", "cuisine": "Chinese", "needs": ["Cauliflower", "Maida", "Soy Sauce", "Ginger"], "steps": "1. Batter fry cauliflower florets. 2. Make a sauce with ginger, garlic, and soy sauce. 3. Toss florets in sauce. 4. Garnish with spring onions."},
    {"name": "White Sauce Pasta", "cuisine": "Continental", "needs": ["Pasta", "Milk", "Butter", "Cheese", "Maida"], "steps": "1. Boil pasta. 2. Make roux with butter and maida. 3. Add milk slowly to make sauce. 4. Add cheese and pasta."},
    {"name": "Dal Tadka", "cuisine": "Indian", "needs": ["Tur Dal", "Tomatoes", "Garlic", "Cumin Seeds"], "steps": "1. Pressure cook dal. 2. Prepare tadka with oil, cumin, and garlic. 3. Add tomatoes and spices. 4. Mix with dal and simmer."}
]

# --- 2. Session State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = ["Onions", "Tomatoes", "Rice", "Turmeric"] # Default items

# --- 3. The UI Layout ---
st.title("🌶️ Punekar Kitchen Pro")

# Sidebar for adding new items from the 100s available
with st.sidebar:
    st.header("➕ Add to Pantry")
    new_item = st.selectbox("Search Ingredients:", [""] + sorted(MASTER_INGREDIENTS))
    if st.button("Add to Kitchen") and new_item != "":
        if new_item not in st.session_state.my_pantry:
            st.session_state.my_pantry.append(new_item)
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear Pantry"):
        st.session_state.my_pantry = []
        st.rerun()

# Main Screen - Current Inventory
st.subheader("Your Current Inventory")
if not st.session_state.my_pantry:
    st.info("Your kitchen is empty! Use the sidebar to add ingredients.")
else:
    # Display pantry as tags
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.my_pantry):
        if cols[i % 3].button(f"❌ {item}", key=f"del_{item}"):
            st.session_state.my_pantry.remove(item)
            st.rerun()

# --- 4. Suggestions Engine ---
st.divider()
cuisine_choice = st.selectbox("What do you want to cook?", ["All", "Maharashtrian", "Indian", "Chinese", "Continental"])

if st.button("🔍 Find Matching Recipes"):
    matches = []
    for r in recipes:
        # Check if we have all 'needs' in our pantry
        has_all = all(item in st.session_state.my_pantry for item in r['needs'])
        if has_all and (cuisine_choice == "All" or r['cuisine'] == cuisine_choice):
            matches.append(r)
    
    if matches:
        st.success(f"Found {len(matches)} recipes you can make right now!")
        for m in matches:
            with st.container():
                st.markdown(f"""
                <div class="recipe-card">
                    <h3>{m['name']} ({m['cuisine']})</h3>
                    <p><strong>Ingredients used:</strong> {', '.join(m['needs'])}</p>
                    <p><strong>Steps:</strong> {m['steps']}</p>
                </div><br>
                """, unsafe_allow_html=True)
    else:
        st.warning("No exact matches found. Add more ingredients to your pantry!")

# --- 5. Automated Shopping List ---
st.divider()
st.subheader("📝 Missing Ingredients")
all_needed = set()
for r in recipes:
    for item in r['needs']:
        all_needed.add(item)

missing = sorted([item for item in all_needed if item not in st.session_state.my_pantry])
if missing:
    st.write("You might need these for other recipes:")
    st.caption(", ".join(missing))
