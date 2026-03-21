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
    .recipe-card { background-color: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #ddd; color: black; margin-bottom: 15px; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); }
    .inventory-tag { background-color: #e8f5e9; padding: 4px 10px; border-radius: 12px; display: inline-block; margin: 2px; border: 1px solid #2e7d32; font-size: 0.85em; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. Master Categories (Expanded) ---
CATEGORIES = {
    "🥦 Veggies": ["Onion", "Tomato", "Potato", "Ginger", "Garlic", "Green Chili", "Coriander", "Curry Leaves", "Lemon", "Cauliflower", "Brinjal", "Okra (Bhindi)", "Spinach", "Methi", "Capsicum", "Carrot", "Beans"],
    "🌾 Grains": ["Atta", "Rice", "Poha", "Besan", "Maida", "Rava", "Jowar Flour", "Sabudana", "Pasta", "Noodles"],
    "🥛 Dairy": ["Milk", "Curd", "Paneer", "Butter", "Ghee", "Cheese Slices", "Cheese Cubes", "Fresh Cream", "Eggs"],
    "🧂 Spices/Sauces": ["Salt", "Turmeric", "Red Chili Powder", "Cumin Seeds", "Mustard Seeds", "Hing", "Kanda Lasun Masala", "Goda Masala", "Tomato Ketchup", "Soy Sauce", "Schezwan Sauce"]
}

recipes = [
    {"name": "Sabudana Khichdi", "needs": ["Sabudana", "Potato"], "cuisine": "Maharashtrian", "steps": "Soak sabudana, sauté with cumin and potatoes. Skip peanuts for safety."},
    {"name": "Cheese Chili Toast", "needs": ["Bread", "Cheese Slices"], "cuisine": "Quick & Tired", "steps": "Toast bread, top with ketchup, cheese, and chilies. Grill."},
    {"name": "Pithla Bhakri", "needs": ["Besan", "Onion", "Jowar Flour"], "cuisine": "Maharashtrian", "steps": "Make besan slurry, sauté with onions/garlic until thick. Serve with Bhakri."},
    {"name": "Mini Paneer Tikka", "needs": ["Paneer", "Curd"], "cuisine": "Kid's Special", "steps": "Marinate paneer in curd and turmeric. Pan fry in ghee."}
]

# --- 2. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Rice", "Onion", "Tomato"])
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
    
    st.divider()
    st.header("🛡️ Safe Swaps")
    st.caption("• No Peanuts/Cashews\n• No Eggs/Seafood")

# --- 4. Main Dashboard ---
st.title("🌶️ Punekar Kitchen Pro")

# Pantry Overview
with st.expander(f"📦 Kitchen Inventory ({len(st.session_state.my_pantry)} items)", expanded=False):
    p_list = sorted(list(st.session_state.my_pantry))
    for p in p_list:
        st.markdown(f'<div class="inventory-tag">{p}</div>', unsafe_allow_html=True)

# Suggestions Logic
st.divider()
st.subheader("What's for a meal?")
mode = st.radio("Style:", ["All", "Quick & Tired", "Kid's Special", "Maharashtrian", "Indian"], horizontal=True)

if st.button("🔍 Suggest Safe Meals"):
    matches = [r for r in recipes if all(i in st.session_state.my_pantry for i in r['needs'])]
    if mode != "All":
        matches = [r for r in matches if r['cuisine'] == mode]
    
    if matches:
        for m in matches:
            rating = st.session_state.ratings.get(m['name'], "Not rated yet")
            st.markdown(f"""
            <div class="recipe-card">
                <b>{m['name']}</b> ({m['cuisine']})<br>
                <small>⭐ Rating: {rating}</small><br><br>
                <p><b>Steps:</b> {m['steps']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Simple Rating Input
            new_rating = st.select_slider(f"Rate {m['name']}:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=m['name'])
            if st.button(f"Save Rating for {m['name']}"):
                st.session_state.ratings[m['name']] = new_rating
                st.rerun()
    else:
        st.warning("Not enough ingredients for this style.")

# --- 5. WhatsApp Shopping List (Shared Choice) ---
all_possible_needs = set([i for r in recipes for i in r['needs']])
missing = sorted([i for i in all_possible_needs if i not in st.session_state.my_pantry])

if missing:
    st.divider()
    st.subheader("📝 Shopping List")
    st.write(", ".join(missing))
    
    # NEUTRAL WHATSAPP MESSAGE
    shop_text = "🛒 *Kitchen Shopping List:*\n"
    shop_text += "Missing items to be picked up:\n\n"
    for item in missing:
        shop_text += f"✅ {item}\n"
    
    encoded_text = urllib.parse.quote(shop_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    
    # Neutral button text
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 Share Shopping List via WhatsApp</a>', unsafe_allow_html=True)
