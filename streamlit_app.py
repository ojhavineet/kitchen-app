import streamlit as st
import urllib.parse

# --- 1. App Config ---
st.set_page_config(page_title="My Kitchen", page_icon="chef_icon.png", layout="centered")

# --- 2. Master 250+ Item List ---
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

# --- 3. Recipe Database ---
recipes = [
    {"name": "Quick Masala Poha", "needs": ["Poha (Thick)", "Onion", "Green Chili", "Turmeric"], "steps": "Wash Poha. Sauté onions/chilies. Add turmeric. Steam 2 mins.", "cuisine": "Quick & Tired"},
    {"name": "Vangi Bhaji", "needs": ["Brinjal", "Onion", "Goda Masala"], "steps": "Sauté onions and brinjal with Goda Masala. Cook until soft.", "cuisine": "Maharashtrian"},
    {"name": "Pithla", "needs": ["Besan", "Onion", "Garlic", "Green Chili"], "steps": "Make besan slurry. Sauté garlic/onions. Cook until thick.", "cuisine": "Maharashtrian"},
    {"name": "Sabudana Khichdi", "needs": ["Sabudana", "Potato", "Green Chili"], "steps": "Sauté cumin/potatoes. Add soaked sabudana. (No peanuts).", "cuisine": "Maharashtrian"},
    {"name": "Schezwan Paneer", "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion"], "steps": "Sauté capsicum/onions. Add sauce and paneer. Toss well.", "cuisine": "Chinese"},
    {"name": "Moong Dal Paratha", "needs": ["Atta", "Moong Dal", "Ghee"], "steps": "Stuff cooked moong dal into atta dough. Roast with Ghee.", "cuisine": "Lunchbox Idea"}
]

# --- 4. Persistent State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = ["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato"]
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- 5. Sidebar: INVENTORY CONTROL (FIXED) ---
with st.sidebar:
    st.header("📦 Inventory Management")
    
    # ADD SECTION
    with st.expander("➕ Add New Stock", expanded=True):
        cat = st.selectbox("Category:", list(CATEGORIES.keys()))
        selected = st.multiselect(f"Select from {cat}:", CATEGORIES[cat])
        if st.button("Add to Kitchen"):
            for item in selected:
                if item not in st.session_state.my_pantry:
                    st.session_state.my_pantry.append(item)
            st.rerun()

    # MANAGE SECTION - FIXED: Always visible, properly deletable
    st.subheader("📝 Current Stock")
    items_to_show = sorted(st.session_state.my_pantry)
    for item in items_to_show:
        cols = st.columns([4, 1])
        cols[0].write(f"• {item}")
        if cols[1].button("X", key=f"del_{item}"):
            st.session_state.my_pantry.remove(item)
            st.rerun()

    st.divider()
    if st.button("🗑️ Reset Entire Pantry"):
        st.session_state.my_pantry = ["Salt", "Turmeric"]
        st.rerun()

# --- 6. Main Header ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("chef_icon.png", width=75)
with col2:
    st.title("My Kitchen")

# --- 7. Search & Suggest ---
st.divider()
view_mode = st.radio("What's the plan?", ["Suggest based on ingredients", "Search for a dish"], horizontal=True)

if view_mode == "Suggest based on ingredients":
    st.subheader("👨‍🍳 Ready to Cook Now")
    ready = [r for r in recipes if all(need in st.session_state.my_pantry for need in r['needs'])]
    if ready:
        for r in ready:
            rating = st.session_state.ratings.get(r['name'], "Not rated yet")
            with st.expander(f"✅ {r['name']} ({rating})", expanded=False):
                st.write(f"**Instructions:** {r['steps']}")
                new_r = st.select_slider(f"Rate {r['name']}:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=r['name'])
                if st.button("Save Rating", key=f"rate_{r['name']}"):
                    st.session_state.ratings[r['name']] = new_r
                    st.rerun()
    else:
        st.info("Nothing is 100% ready. Switch to 'Search' to see what you need.")

else:
    st.subheader("🔍 Search for a Dish")
    query = st.text_input("Type dish name...", placeholder="Poha, Paneer...").strip().lower()
    if query:
        results = [r for r in recipes if query in r['name'].lower()]
        for r in results:
            missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
            rating = st.session_state.ratings.get(r['name'], "Not rated yet")
            with st.expander(f"📖 {r['name']} ({rating})", expanded=True):
                st.write(f"**Detailed Recipe:** {r['steps']}")
                if not missing:
                    st.success("✅ All set!")
                else:
                    st.warning(f"⚠️ Missing: {', '.join(missing)}")
                    if st.button(f"🛒 Add missing to Shopping List", key=f"add_{r['name']}"):
                        for i in missing:
                            if i not in st.session_state.shopping_list:
                                st.session_state.shopping_list.append(i)
                        st.rerun()

# --- 8. SHOPPING LIST & WHATSAPP (FIXED) ---
# Clean list: remove things if they were added to pantry
st.session_state.shopping_list = [i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry]

if st.session_state.shopping_list:
    st.divider()
    st.subheader("📝 Your Shopping List")
    
    for item in sorted(st.session_state.shopping_list):
        st.write(f"✅ {item}")
    
    # WhatsApp Button - BIG and BOLD
    msg = "🛒 *Kitchen List:* " + ", ".join(st.session_state.shopping_list)
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    
    st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
        <div style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;font-size:1.2em;box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
            📲 Share Shopping List via WhatsApp
        </div>
    </a>
    ''', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear List"):
        st.session_state.shopping_list = []
        st.rerun()
