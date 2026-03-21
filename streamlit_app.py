import streamlit as st
import random
import urllib.parse

# --- 1. App Configuration ---
st.set_page_config(
    page_title="Punekar Kitchen Pro", 
    page_icon="chef_icon.png", 
    layout="centered"
)

# --- 2. Styling ---
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

# --- 3. THE 250+ ITEM CATEGORIZED MASTER LIST ---
CATEGORIES = {
    "🥦 Veggies": ["Onion", "Tomato", "Potato", "Ginger", "Garlic", "Green Chili", "Coriander", "Curry Leaves", "Lemon", "Cauliflower", "Cabbage", "Capsicum", "Carrot", "French Beans", "Brinjal", "Okra (Bhindi)", "Bottle Gourd", "Ridge Gourd", "Bitter Gourd", "Pumpkin", "Drumstick", "Spring Onion", "Sweet Potato", "Mint", "Spinach", "Methi", "Radish", "Cucumber", "Beetroot", "Corn", "Mushroom", "Broccoli", "Colocasia Leaves", "Ivy Gourd (Tondli)"],
    "🌾 Grains/Flours": ["Atta", "Rice (Basmati)", "Rice (Indrayani)", "Poha (Thick)", "Poha (Thin)", "Besan", "Maida", "Rava (Suji)", "Jowar Flour", "Bajra Flour", "Nachni Flour", "Sabudana", "Corn Flour", "Vermicelli", "Oats"],
    "🥣 Dals/Pulses": ["Tur Dal", "Moong Dal", "Chana Dal", "Urad Dal", "Masoor Dal", "Matki", "Kabuli Chana", "Kala Chana", "Rajma", "Green Moong", "Chowli"],
    "🥛 Dairy/Cold": ["Milk", "Curd", "Paneer", "Butter", "Ghee", "Cheese Slices", "Cheese Cubes", "Fresh Cream", "Eggs", "Buttermilk"],
    "🥫 Sauces/Pantry": ["Tomato Ketchup", "Soy Sauce", "Green Chili Sauce", "Red Chili Sauce", "Vinegar", "Schezwan Sauce", "Pasta Sauce", "Mayonnaise", "Honey", "Jaggery", "Sugar", "Tea", "Coffee", "Bournvita", "Jam", "Pickle"],
    "🧂 Spices": ["Salt", "Turmeric", "Red Chili Powder", "Coriander Powder", "Cumin Seeds", "Mustard Seeds", "Hing", "Kanda Lasun Masala", "Goda Masala", "Garam Masala", "Kasuri Methi", "Ajwain", "Black Pepper", "Chat Masala", "Sambhar Powder", "Pav Bhaji Masala"],
    "🥜 Nuts/Dry Fruits": ["Peanuts", "Cashews", "Almonds", "Walnuts", "Sesame Seeds (Til)", "Sunflower Seeds", "Dates"],
    "🧼 Cleaning/Utility": ["Dishwash Soap", "Handwash", "Detergent", "Floor Cleaner", "Garbage Bags", "Kitchen Rolls", "Foil"]
}

# --- 4. Recipe Database ---
recipes = [
    {"name": "Quick Masala Poha", "cuisine": "Quick & Tired", "needs": ["Poha (Thick)", "Onion", "Green Chili"], "allergens": ["Peanuts"], "steps": "Wash poha. Sauté onions and chilies. Add turmeric. Steam for 2 mins."},
    {"name": "Vangi Bhaji (Brinjal)", "cuisine": "Maharashtrian", "needs": ["Brinjal", "Onion", "Goda Masala"], "allergens": [], "steps": "Sauté onions and brinjal with Goda Masala. Simmer until soft."},
    {"name": "Pithla Bhakri", "cuisine": "Maharashtrian", "needs": ["Besan", "Onion", "Garlic", "Jowar Flour"], "allergens": [], "steps": "Make besan slurry. Sauté garlic/onions. Cook until thick. Serve with Bhakri."},
    {"name": "Schezwan Paneer", "cuisine": "Chinese", "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion"], "allergens": [], "steps": "Sauté onions and capsicum. Add schezwan sauce and paneer cubes."},
    {"name": "Moong Dal Paratha", "cuisine": "Lunchbox Idea", "needs": ["Atta", "Moong Dal", "Ghee"], "allergens": [], "steps": "Stuff paratha with cooked dal. Stays soft for lunch!"},
    {"name": "Sabudana Khichdi", "cuisine": "Maharashtrian", "needs": ["Sabudana", "Potato", "Green Chili"], "allergens": ["Peanuts"], "steps": "Sauté soaked sabudana with potatoes. Skip peanuts for safety."},
    {"name": "Mini Cheese Uttapam", "cuisine": "Kid's Special", "needs": ["Rice (Indrayani)", "Cheese Cubes", "Tomato"], "allergens": [], "steps": "Small rice pancakes topped with tomatoes and cheese."}
]

# --- 5. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato"])
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = set()
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- 6. Sidebar (Update Kitchen) ---
with st.sidebar:
    st.header("🏠 Family Profile")
    st.write("**Avoiding for Dviti:** Peanuts, Cashews, Eggs, Seafood")
    st.divider()
    
    st.header("➕ Update Kitchen Stock")
    cat = st.selectbox("Select Category:", list(CATEGORIES.keys()))
    selected_items = st.multiselect(f"Items in {cat}:", CATEGORIES[cat])
    
    if st.button("Add Selected to Kitchen"):
        for item in selected_items:
            st.session_state.my_pantry.add(item)
        st.success("Kitchen Updated!")
        st.rerun()
    
    if st.button("🗑️ Reset All Items"):
        st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil"])
        st.rerun()

# --- 7. Main Interface Header ---
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("chef_icon.png", width=80)
    except:
        st.write("🍳")

with col2:
    st.title("Punekar Kitchen Pro")

# Pantry Overview
with st.expander(f"📦 Our Kitchen Inventory ({len(st.session_state.my_pantry)} items)", expanded=False):
    p_list = sorted(list(st.session_state.my_pantry))
    for p in p_list:
        st.markdown(f'<div class="inventory-tag">{p}</div>', unsafe_allow_html=True)

# --- 8. Suggestions & Smart Shopping List ---
st.divider()
st.subheader("Find a Meal")
mode = st.radio("Style:", ["All", "Quick & Tired", "Kid's Special", "Lunchbox Idea", "Maharashtrian", "Chinese", "Indian"], horizontal=True)

# Process Recipes
for r in recipes:
    if mode == "All" or r['cuisine'] == mode:
        # Check ingredients
        missing_for_this = [i for i in r['needs'] if i not in st.session_state.my_pantry]
        rating = st.session_state.ratings.get(r['name'], "Not rated yet")
        
        with st.container():
            st.markdown(f'<div class="recipe-card"><h3>{r["name"]}</h3><small>⭐ Rating: {rating}</small>', unsafe_allow_html=True)
            
            if not missing_for_this:
                st.success("✅ You have all ingredients!")
                st.write(f"**Instructions:** {r['steps']}")
                
                # Rating Input
                new_rating = st.select_slider(f"Rate {r['name']}:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=r['name'])
                if st.button(f"Save Rating for {r['name']}"):
                    st.session_state.ratings[r['name']] = new_rating
                    st.rerun()
            else:
                st.warning(f"⚠️ Missing: {', '.join(missing_for_this)}")
                if st.button(f"🛒 Add missing for {r['name']} to List", key=r['name']):
                    for i in missing_for_this: st.session_state.shopping_list.add(i)
                    st.toast(f"Added to Shopping List!")
            st.markdown('</div>', unsafe_allow_html=True)

# --- 9. WhatsApp Export (Only shows items she actually added) ---
# Clean shopping list: Remove items if they were added to pantry
st.session_state.shopping_list = {i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry}

if st.session_state.shopping_list:
    st.divider()
    st.subheader("📝 Your Shopping List")
    st.write(", ".join(sorted(st.session_state.shopping_list)))
    
    shop_text = "🛒 *Kitchen Shopping List:*\n"
    for item in sorted(st.session_state.shopping_list):
        shop_text += f"✅ {item}\n"
    
    encoded_text = urllib.parse.quote(shop_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 Share List via WhatsApp</a>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Shopping List"):
        st.session_state.shopping_list = set()
        st.rerun()
