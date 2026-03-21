import streamlit as st
import urllib.parse

# --- 1. App Config ---
st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="chef_icon.png", layout="centered")

# --- 2. Master Categorized List (250+ Items) ---
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

# --- 3. Detailed Recipes ---
recipes = [
    {"name": "Quick Masala Poha", "needs": ["Poha (Thick)", "Onion", "Green Chili", "Turmeric"], "steps": "Wash Poha. Sauté onions/chilies. Add turmeric. Steam 2 mins.", "cuisine": "Quick & Tired"},
    {"name": "Vangi Bhaji", "needs": ["Brinjal", "Onion", "Goda Masala"], "steps": "Sauté onions and brinjal with Goda Masala. Cook until soft.", "cuisine": "Maharashtrian"},
    {"name": "Pithla", "needs": ["Besan", "Onion", "Garlic", "Green Chili"], "steps": "Make besan slurry. Sauté garlic/onions. Cook until thick.", "cuisine": "Maharashtrian"},
    {"name": "Sabudana Khichdi", "needs": ["Sabudana", "Potato", "Green Chili"], "steps": "Sauté cumin/potatoes. Add soaked sabudana. (No peanuts).", "cuisine": "Maharashtrian"},
    {"name": "Schezwan Paneer", "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion"], "steps": "Sauté capsicum/onions. Add sauce and paneer. Toss well.", "cuisine": "Chinese"},
    {"name": "Moong Dal Paratha", "needs": ["Atta", "Moong Dal", "Ghee"], "steps": "Stuff cooked moong dal into atta dough. Roast with Ghee.", "cuisine": "Lunchbox Idea"}
]

# --- 4. State Management (List based for better UI reactivity) ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = ["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato"]
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- 5. Sidebar: Inventory Control (FIXED) ---
with st.sidebar:
    st.header("📦 Manage Kitchen")
    
    # 5a. ADD Items
    with st.expander("➕ Add Items", expanded=True):
        cat = st.selectbox("Category:", list(CATEGORIES.keys()))
        selected = st.multiselect(f"Pick from {cat}:", CATEGORIES[cat])
        if st.button("Add to Pantry"):
            for item in selected:
                if item not in st.session_state.my_pantry:
                    st.session_state.my_pantry.append(item)
            st.rerun()

    # 5b. REMOVE Items (FIXED LIST)
    st.subheader("📝 In Stock")
    pantry_sorted = sorted(st.session_state.my_pantry)
    for item in pantry_sorted:
        c1, c2 = st.columns([5, 1])
        c1.write(f"• {item}")
        # The key must be unique and specific to the item
        if c2.button("X", key=f"del_sidebar_{item}"):
            st.session_state.my_pantry.remove(item)
            st.rerun()

    if st.button("🗑️ Reset All"):
        st.session_state.my_pantry = ["Salt", "Turmeric"]
        st.rerun()

# --- 6. Main Header ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("chef_icon.png", width=75)
with col2:
    st.title("Punekar Kitchen Pro")

# --- 7. Main Body ---
st.divider()
tab1, tab2 = st.tabs(["💡 Suggestions", "🔍 Search Dish"])

with tab1:
    st.subheader("Ready to Cook (100% Match)")
    # Logic: Only show if every required ingredient is in pantry
    ready = [r for r in recipes if all(need in st.session_state.my_pantry for need in r['needs'])]
    if ready:
        for r in ready:
            rating = st.session_state.ratings.get(r['name'], "⭐⭐⭐")
            with st.expander(f"✅ {r['name']} ({rating})", expanded=False):
                st.write(f"**Instructions:** {r['steps']}")
                new_rate = st.select_slider(f"Rate:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=f"rate_tab1_{r['name']}")
                if st.button("Save", key=f"btn_tab1_{r['name']}"):
                    st.session_state.ratings[r['name']] = new_rate
                    st.rerun()
    else:
        st.info("No 100% matches. Add items or use Search.")

with tab2:
    st.subheader("Look up a Dish")
    query = st.text_input("What are you looking for?", placeholder="e.g. Poha").strip().lower()
    if query:
        results = [r for r in recipes if query in r['name'].lower()]
        for r in results:
            missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
            with st.expander(f"📖 {r['name']}", expanded=True):
                st.write(f"**Recipe:** {r['steps']}")
                if not missing:
                    st.success("✅ All set!")
                else:
                    st.warning(f"⚠️ Missing: {', '.join(missing)}")
                    if st.button(f"🛒 Add missing to Shopping List", key=f"add_shopp_{r['name']}"):
                        for m_item in missing:
                            if m_item not in st.session_state.shopping_list:
                                st.session_state.shopping_list.append(m_item)
                        st.rerun()

# --- 8. Persistent Shopping List & WhatsApp ---
# Clean: remove items if they are now in the pantry
st.session_state.shopping_list = [i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry]

if st.session_state.shopping_list:
    st.divider()
    st.subheader("📋 Your Shopping List")
    shop_items = sorted(st.session_state.shopping_list)
    for s_item in shop_items:
        st.write(f"- {s_item}")
    
    # WhatsApp - Neutral & Large
    whatsapp_msg = "🛒 *Kitchen Shopping List:* " + ", ".join(shop_items)
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(whatsapp_msg)}"
    
    st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
        <div style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;font-size:1.1em;box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
            📲 Share List via WhatsApp
        </div>
    </a>
    ''', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Shopping List"):
        st.session_state.shopping_list = []
        st.rerun()
