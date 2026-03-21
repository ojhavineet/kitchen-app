import streamlit as st
import urllib.parse

# --- 1. App Config ---
st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="chef_icon.png", layout="centered")

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
    {"name": "Quick Masala Poha", "needs": ["Poha (Thick)", "Onion", "Green Chili"], "steps": "Wash poha. Sauté onions/chilies. Steam 2 mins."},
    {"name": "Vangi Bhaji", "needs": ["Brinjal", "Onion", "Goda Masala"], "steps": "Sauté onions and brinjal with Goda Masala."},
    {"name": "Sabudana Khichdi", "needs": ["Sabudana", "Potato", "Green Chili"], "steps": "Sauté soaked sabudana with potatoes. Skip peanuts for Dviti."},
    {"name": "Moong Dal Paratha", "needs": ["Atta", "Moong Dal", "Ghee"], "steps": "Stuff paratha with cooked dal and fry with ghee."},
    {"name": "Schezwan Paneer", "needs": ["Paneer", "Schezwan Sauce", "Capsicum"], "steps": "Sauté capsicum. Add sauce and paneer cubes."}
]

# --- 4. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato"])
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = set()

# --- 5. Main UI Header ---
col1, col2 = st.columns([1, 5])
with col1:
    try: st.image("chef_icon.png", width=70)
    except: st.write("🍳")
with col2: st.title("Punekar Kitchen Pro")

# --- 6. Sidebar: The Inventory Is Back! ---
with st.sidebar:
    st.header("📦 Inventory Management")
    with st.expander("➕ Add Stock (Categorized)", expanded=True):
        cat = st.selectbox("Choose Category:", list(CATEGORIES.keys()))
        selected = st.multiselect(f"Select {cat}:", CATEGORIES[cat])
        if st.button("Add to Kitchen"):
            for item in selected: st.session_state.my_pantry.add(item)
            st.rerun()
    
    st.divider()
    st.subheader("🛒 Current Stock")
    st.write(", ".join(sorted(st.session_state.my_pantry)))
    if st.button("🗑️ Clear Entire Kitchen"):
        st.session_state.my_pantry = set(["Salt", "Turmeric"])
        st.rerun()

# --- 7. Main Functionality ---
st.divider()
view_mode = st.radio("What's the plan?", ["Suggest based on ingredients", "Search for a dish"], horizontal=True)

if view_mode == "Suggest based on ingredients":
    st.subheader("👨‍ Chef's Suggestions")
    ready = [r for r in recipes if set(r['needs']).issubset(st.session_state.my_pantry)]
    if ready:
        for r in ready:
            with st.expander(f"✅ Ready: {r['name']}", expanded=False):
                st.write(f"**Steps:** {r['steps']}")
    else:
        st.info("Nothing is 100% ready. Switch to 'Search' to see what to buy!")

else:
    st.subheader("🔍 Search for a Dish")
    query = st.text_input("Type here...", placeholder="Poha, Paneer, Paratha...").strip().lower()
    if query:
        results = [r for r in recipes if query in r['name'].lower()]
        for r in results:
            missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
            with st.expander(f"📖 {r['name']}", expanded=True):
                if not missing: st.success("✅ All set!")
                else:
                    st.warning(f"⚠️ Missing: {', '.join(missing)}")
                    if st.button(f"Add missing to List", key=r['name']):
                        for i in missing: st.session_state.shopping_list.add(i)
                        st.toast("List updated!")

# --- 8. Shopping List ---
if st.session_state.shopping_list:
    st.session_state.shopping_list = {i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry}
    if st.session_state.shopping_list:
        st.divider()
        st.subheader("🛒 Shopping List")
        items = "\n".join([f"- {i}" for i in sorted(st.session_state.shopping_list)])
        st.info(items)
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote('🛒 *Kitchen List:*' + items)}"
        st.markdown(f'''<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366;color:white;padding:12px;border-radius:10px;text-align:center;font-weight:bold;">📲 WhatsApp List</div></a>''', unsafe_allow_html=True)
