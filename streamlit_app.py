import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="🌶️", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; height: 3.5em; font-weight: bold; }
    .whatsapp-btn { 
        display: block; width: 100%; text-align: center; background-color: #25D366; 
        color: white !important; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 20px;
    }
    .recipe-card { background-color: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #ddd; color: black; margin-bottom: 15px; }
    .inventory-tag { background-color: #e8f5e9; padding: 4px 10px; border-radius: 12px; display: inline-block; margin: 2px; border: 1px solid #2e7d32; font-size: 0.85em; color: black; }
    .rating-box { background-color: #fff9db; padding: 10px; border-radius: 8px; border: 1px solid #fcc419; margin-top: 10px; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. Master Data ---
CATEGORIES = {
    "🥦 Veggies": ["Onion", "Tomato", "Potato", "Ginger", "Garlic", "Green Chili", "Coriander", "Curry Leaves", "Lemon", "Cauliflower", "Brinjal", "Okra (Bhindi)", "Spinach", "Methi"],
    "🌾 Grains": ["Atta", "Rice", "Poha", "Besan", "Maida", "Rava", "Jowar Flour", "Sabudana"],
    "🥛 Dairy": ["Milk", "Curd", "Paneer", "Butter", "Ghee", "Cheese Slices", "Cheese Cubes", "Eggs"],
    "🧂 Spices": ["Salt", "Turmeric", "Red Chili Powder", "Cumin Seeds", "Mustard Seeds", "Hing", "Kanda Lasun Masala", "Goda Masala"]
}

recipes = [
    {"name": "Sabudana Khichdi", "needs": ["Sabudana", "Potato"], "cuisine": "Maharashtrian"},
    {"name": "Cheese Chili Toast", "needs": ["Bread", "Cheese Slices"], "cuisine": "Quick & Tired"},
    {"name": "Pithla Bhakri", "needs": ["Besan", "Onion", "Jowar Flour"], "cuisine": "Maharashtrian"},
    {"name": "Mini Paneer Tikka", "needs": ["Paneer", "Curd"], "cuisine": "Kid's Special"}
]

# --- 2. State Management (Added Ratings) ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Rice", "Onion", "Tomato", "Potato", "Sabudana", "Besan", "Jowar Flour"])
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- 3. Sidebar ---
with st.sidebar:
    st.header("🏪 Add Stock")
    cat = st.selectbox("Category:", list(CATEGORIES.keys()))
    selected = st.multiselect(f"Pick items:", CATEGORIES[cat])
    if st.button("Add to Kitchen"):
        for item in selected: st.session_state.my_pantry.add(item)
        st.rerun()

# --- 4. Main Dashboard ---
st.title("🌶️ Punekar Kitchen Pro")

# Suggestions Logic
st.subheader("What's for a meal?")
mode = st.radio("Style:", ["All", "Quick & Tired", "Kid's Special", "Maharashtrian", "Indian"], horizontal=True)

if st.button("🔍 Suggest Safe Meals"):
    matches = [r for r in recipes if all(i in st.session_state.my_pantry for i in r['needs'])]
    if mode != "All":
        matches = [r for r in matches if r['cuisine'] == mode]
    
    if matches:
        for m in matches:
            rating = st.session_state.ratings.get(m['name'], "No rating yet")
            st.markdown(f"""
            <div class="recipe-card">
                <b>{m['name']}</b> ({m['cuisine']})<br>
                <span style="font-size:0.8em; color:#666;">⭐ Current Rating: {rating}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Simple Rating Input
            new_rating = st.select_slider(f"Rate {m['name']}:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=m['name'])
            if st.button(f"Save Rating for {m['name']}"):
                st.session_state.ratings[m['name']] = new_rating
                st.success("Rating saved!")
    else:
        st.warning("Not enough items in pantry.")

# --- 5. Top Rated (Wife's Favorite List) ---
if st.session_state.ratings:
    st.divider()
    st.subheader("🏆 Dviti's Favorites")
    for meal, stars in st.session_state.ratings.items():
        if "⭐⭐⭐⭐" in stars:
            st.write(f"{stars} - {meal}")

# --- 6. WhatsApp Sync ---
all_possible_needs = set([i for r in recipes for i in r['needs']])
missing = sorted([i for i in all_possible_needs if i not in st.session_state.my_pantry])

if missing:
    st.divider()
    shop_text = "🛒 *Kitchen List:*\n" + "\n".join([f"✅ {i}" for i in missing])
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(shop_text)}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 WhatsApp List to Husband</a>', unsafe_allow_html=True)
