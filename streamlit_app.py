import streamlit as st
import random
import urllib.parse

st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="chef_icon.png", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; height: 3.5em; font-weight: bold; }
    .whatsapp-btn { display: block; width: 100%; text-align: center; background-color: #25D366; color: white !important; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 10px; }
    .recipe-card { background-color: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #ddd; color: black; margin-bottom: 15px; }
    .shopping-box { background-color: #fff5f5; padding: 15px; border-radius: 10px; border: 1px solid #feb2b2; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil"])
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = set()

# --- 2. Master Categories (Partial list for brevity) ---
CATEGORIES = {"🥦 Veggies": ["Onion", "Tomato", "Potato", "Ginger", "Garlic", "Brinjal", "Okra"], "🌾 Grains": ["Atta", "Rice", "Poha", "Besan"]}

# --- 3. Sidebar ---
with st.sidebar:
    st.header("🏪 Update Kitchen")
    cat = st.selectbox("Category:", list(CATEGORIES.keys()))
    selected = st.multiselect("Items in Kitchen:", CATEGORIES[cat])
    if st.button("Add to Kitchen"):
        for item in selected: st.session_state.my_pantry.add(item)
        st.rerun()

# --- 4. Main UI ---
col1, col2 = st.columns([1, 5])
with col1: st.image("chef_icon.png", width=70)
with col2: st.title("Punekar Kitchen Pro")

# --- 5. Recipe Suggestion Engine ---
recipes = [
    {"name": "Vangi Bhaji", "needs": ["Brinjal", "Onion"], "cuisine": "Maharashtrian"},
    {"name": "Pithla", "needs": ["Besan", "Onion", "Garlic"], "cuisine": "Maharashtrian"}
]

st.subheader("Find a Meal")
mode = st.radio("Style:", ["All", "Maharashtrian", "Quick & Tired"], horizontal=True)

# Find what we CAN cook and what we are MISSING
for r in recipes:
    if mode == "All" or r['cuisine'] == mode:
        missing_for_this = [i for i in r['needs'] if i not in st.session_state.my_pantry]
        
        with st.container():
            st.markdown(f'<div class="recipe-card"><b>{r["name"]}</b>', unsafe_allow_html=True)
            if not missing_for_this:
                st.success("✅ You have all ingredients!")
            else:
                st.warning(f"⚠️ Missing: {', '.join(missing_for_this)}")
                if st.button(f"🛒 Add missing for {r['name']} to List", key=r['name']):
                    for i in missing_for_this: st.session_state.shopping_list.add(i)
                    st.toast(f"Added to Shopping List!")
            st.markdown('</div>', unsafe_allow_html=True)

# --- 6. The "Smart" Shopping List (Only shows what she added) ---
if st.session_state.shopping_list:
    st.divider()
    st.subheader("📝 Your Shopping List")
    
    # Remove items from shopping list if they were just added to pantry
    st.session_state.shopping_list = {i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry}
    
    if st.session_state.shopping_list:
        items_text = ", ".join(sorted(st.session_state.shopping_list))
        st.write(items_text)
        
        # WhatsApp Export
        shop_text = "🛒 *Kitchen Shopping List:*\n" + "\n".join([f"- {i}" for i in st.session_state.shopping_list])
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(shop_text)}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 Share List via WhatsApp</a>', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Shopping List"):
            st.session_state.shopping_list = set()
            st.rerun()
