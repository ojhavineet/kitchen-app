import streamlit as st
import urllib.parse

# --- 1. App Config & Icon ---
st.set_page_config(
    page_title="Punekar Kitchen Pro", 
    page_icon="chef_icon.png", 
    layout="centered"
)

# --- 2. Master 250+ Item List (Categorized) ---
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

# --- 3. Detailed Recipe Database ---
recipes = [
    {"name": "Quick Masala Poha", "needs": ["Poha (Thick)", "Onion", "Green Chili", "Turmeric"], "steps": "1. Wash Poha. 2. Sauté onions, chilies, and curry leaves. 3. Add turmeric and salt. 4. Mix in Poha, cover and steam for 2 mins.", "cuisine": "Quick & Tired"},
    {"name": "Vangi Bhaji", "needs": ["Brinjal", "Onion", "Goda Masala"], "steps": "1. Slice Brinjal. 2. Sauté onions. 3. Add Goda Masala and Brinjal. 4. Cover and cook until soft.", "cuisine": "Maharashtrian"},
    {"name": "Pithla", "needs": ["Besan", "Onion", "Garlic", "Green Chili"], "steps": "1. Mix Besan and water into a slurry. 2. Sauté garlic, onions, and chilies. 3. Pour in slurry and stir until thick.", "cuisine": "Maharashtrian"},
    {"name": "Sabudana Khichdi", "needs": ["Sabudana", "Potato", "Green Chili"], "steps": "1. Sauté cumin and potatoes. 2. Add soaked sabudana and chilies. 3. Cook until translucent. (Peanuts skipped for Dviti).", "cuisine": "Maharashtrian"},
    {"name": "Schezwan Paneer", "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion"], "steps": "1. Sauté capsicum and onions. 2. Add Schezwan sauce and paneer cubes. 3. Toss until coated.", "cuisine": "Chinese"},
    {"name": "Moong Dal Paratha", "needs": ["Atta", "Moong Dal", "Ghee"], "steps": "1. Stuff cooked moong dal into atta dough. 2. Roll and roast on tawa with Ghee until golden.", "cuisine": "Lunchbox Idea"}
]

# --- 4. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato"])
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = set()
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- 5. Custom UI Header ---
col1, col2 = st.columns([1, 5])
with col1:
    try: st.image("chef_icon.png", width=75)
    except: st.write("🍳")
with col2: st.title("Punekar Kitchen Pro")

# --- 6. Sidebar: Inventory Control (Add & Remove) ---
with st.sidebar:
    st.header("📦 Inventory Management")
    
    # ADD SECTION
    with st.expander("➕ Add New Stock", expanded=True):
        cat = st.selectbox("Category:", list(CATEGORIES.keys()))
        selected = st.multiselect(f"Select from {cat}:", CATEGORIES[cat])
        if st.button("Add to Kitchen"):
            for item in selected: st.session_state.my_pantry.add(item)
            st.rerun()
    
    # MANAGE SECTION
    with st.expander("📝 Manage/Remove Items", expanded=False):
        current_items = sorted(list(st.session_state.my_pantry))
        for item in current_items:
            cols = st.columns([4, 1])
            cols[0].write(f"- {item}")
            if cols[1].button("X", key=f"del_{item}"):
                st.session_state.my_pantry.remove(item)
                st.rerun()

    st.divider()
    if st.button("🗑️ Reset Entire Pantry"):
        st.session_state.my_pantry = set(["Salt", "Turmeric"])
        st.rerun()

# --- 7. Main Dashboard: Suggest vs Search ---
st.divider()
view_mode = st.radio("What's the plan?", ["Suggest based on ingredients", "Search for a dish"], horizontal=True)

if view_mode == "Suggest based on ingredients":
    st.subheader("👨‍🍳 Ready to Cook Now")
    ready = [r for r in recipes if set(r['needs']).issubset(st.session_state.my_pantry)]
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
        st.info("Nothing is 100% ready. Switch to 'Search' to see what you need to buy!")

else:
    st.subheader("🔍 Search for a Dish")
    query = st.text_input("Type dish name...", placeholder="Poha, Paneer, Paratha...").strip().lower()
    if query:
        results = [r for r in recipes if query in r['name'].lower()]
        for r in results:
            missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
            rating = st.session_state.ratings.get(r['name'], "Not rated yet")
            with st.expander(f"📖 {r['name']} ({rating})", expanded=True):
                st.write(f"**Detailed Recipe:** {r['steps']}")
                if not missing: st.success("✅ All set!")
                else:
                    st.warning(f"⚠️ Missing: {', '.join(missing)}")
                    if st.button(f"Add missing to List", key=f"add_{r['name']}"):
                        for i in missing: st.session_state.shopping_list.add(i)
                        st.toast("Updated!")

# --- 8. Smart Shopping List & WhatsApp ---
st.session_state.shopping_list = {i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry}

if st.session_state.shopping_list:
    st.divider()
    st.subheader("🛒 Shopping List")
    items_list = sorted(list(st.session_state.shopping_list))
    st.info("\n".join([f"- {i}" for i in items_list]))
    
    msg = f"🛒 *Kitchen List:* " + ", ".join(items_list)
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'''<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
        <div style="background-color:#25D366;color:white;padding:12px;border-radius:10px;text-align:center;font-weight:bold;">📲 Share Shopping List via WhatsApp</div></a>''', unsafe_allow_html=True)
