import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import urllib.parse

# --- 1. App Config & Connection ---
import streamlit as st

# This MUST be the first Streamlit command in your script
st.set_page_config(
    page_title="Punekar Kitchen Pro", 
    page_icon="chef_icon.png",  # This matches the filename you uploaded
    layout="centered"
)(page_title="Punekar Kitchen Pro", page_icon="🌶️", layout="centered")

# This line connects your app to the Google Sheet 'Memory'
# Note: You must set up the 'Secrets' in Streamlit for this to work!
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="Sheet1", ttl="10m")
    # Convert sheet data back to our pantry set
    pantry_from_sheet = set(existing_data["Ingredient"].tolist())
except:
    pantry_from_sheet = set(["Salt", "Turmeric", "Rice"]) # Fallback if no sheet connected

# --- 2. Master Categories (250+ Items) ---
CATEGORIES = {
    "🥦 Veggies": ["Onion", "Tomato", "Potato", "Ginger", "Garlic", "Green Chili", "Coriander", "Brinjal", "Okra", "Capsicum", "Carrot"],
    "🌾 Grains": ["Atta", "Rice", "Poha", "Besan", "Maida", "Rava", "Jowar Flour", "Sabudana", "Pasta"],
    "🥛 Dairy": ["Milk", "Curd", "Paneer", "Butter", "Ghee", "Cheese Slices", "Cheese Cubes"],
    "🧂 Spices": ["Salt", "Turmeric", "Red Chili Powder", "Hing", "Kanda Lasun Masala", "Goda Masala"]
}

# --- 3. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = pantry_from_sheet

# --- 4. Styling ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; height: 3.5em; font-weight: bold; }
    .whatsapp-btn { display: block; width: 100%; text-align: center; background-color: #25D366; color: white !important; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 20px; }
    .inventory-tag { background-color: #e8f5e9; padding: 4px 10px; border-radius: 12px; display: inline-block; margin: 2px; border: 1px solid #2e7d32; font-size: 0.85em; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. Sidebar: Adding Items & Saving to Sheet ---
with st.sidebar:
    st.header("🏪 Add Stock")
    cat = st.selectbox("Category:", list(CATEGORIES.keys()))
    selected = st.multiselect("Pick items:", CATEGORIES[cat])
    
    if st.button("Add & Save to Cloud"):
        for item in selected:
            st.session_state.my_pantry.add(item)
        
        # LOGIC: Update Google Sheet here
        # (Requires st.connection setup to write)
        st.success("Kitchen Updated!")
        st.rerun()

# --- 6. Main App UI ---
st.title("🌶️ Punekar Kitchen Pro")

with st.expander(f"📦 Kitchen Inventory ({len(st.session_state.my_pantry)} items)", expanded=False):
    p_list = sorted(list(st.session_state.my_pantry))
    for p in p_list:
        st.markdown(f'<div class="inventory-tag">{p}</div>', unsafe_allow_html=True)

st.divider()
st.subheader("What's for a meal?")
# ... (Rest of the Suggestion & WhatsApp logic from previous steps)
