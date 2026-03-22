import streamlit as st
import urllib.parse

# --- 1. SETTINGS & ICON ---
st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="chef_icon.png", layout="centered")

# --- 2. THE 250+ ITEM MASTER LIST ---
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

# --- 3. THE RECIPE DATABASE (With Details) ---
recipes = [
    {"name": "Quick Masala Poha", "needs": ["Poha (Thick)", "Onion", "Green Chili", "Turmeric"], "steps": "Wash Poha. Sauté onions/chilies. Add turmeric. Steam for 2 mins.", "cuisine": "Quick & Tired"},
    {"name": "Vangi Bhaji", "needs": ["Brinjal", "Onion", "Goda Masala"], "steps": "Sauté onions and brinjal with Goda Masala. Cook until soft.", "cuisine": "Maharashtrian"},
    {"name": "Pithla", "needs": ["Besan", "Onion", "Garlic", "Green Chili"], "steps": "Make besan slurry. Sauté garlic/onions. Cook until thick.", "cuisine": "Maharashtrian"},
    {"name": "Sabudana Khichdi", "needs": ["Sabudana", "Potato", "Green Chili"], "steps": "Sauté cumin/potatoes. Add soaked sabudana. (No peanuts for Dviti).", "cuisine": "Maharashtrian"},
    {"name": "Schezwan Paneer", "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion"], "steps": "Sauté capsicum/onions. Add sauce and paneer. Toss well.", "cuisine": "Chinese"},
    {"name": "Moong Dal Paratha", "needs": ["Atta", "Moong Dal", "Ghee"], "steps": "Stuff cooked moong dal into atta dough. Roast with Ghee.", "cuisine": "Lunchbox Idea"}
]

# --- 4. DATA STORAGE ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = ["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato"]
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []

# --- 5. SIDEBAR: INVENTORY MANAGEMENT ---
with st.sidebar:
    st.header("📦 Kitchen Stock")
    
    # ADDING ITEMS
    with st.expander("➕ Add Items", expanded=True):
        cat = st.selectbox("Category:", list(CATEGORIES.keys()))
        selected = st.multiselect(f"Pick {cat}:", CATEGORIES[cat])
        if st.button("Add to Kitchen"):
            for item in selected:
                if item not in st.session_state.my_pantry:
                    st.session_state.my_pantry.append(item)
            st.rerun()

    # REMOVING ITEMS (The specific fix for your screenshot)
    st.subheader("📝 Currently In Stock")
    for item in sorted(st.session_state.my_pantry):
        cols = st.columns([4, 1])
        cols[0].write(f"• {item}")
        # Unique key for every item ensures the button works
        if cols[1].button("X", key=f"remove_{item}"):
            st.session_state.my_pantry.remove(item)
            st.rerun()

# --- 6. MAIN HEADER ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("chef_icon.png", width=75)
with col2:
    st.title("Punekar Kitchen Pro")

# --- 7. MAIN FUNCTIONALITY (Search & Suggestions) ---
st.divider()
option = st.radio("What do you want to do?", ["See what I can cook now", "Search for a specific dish"], horizontal=True)

if option == "See what I can cook now":
    st.subheader("👨‍🍳 Ready to Cook")
    # Logic: Show recipes where all 'needs' are in the pantry
    available = [r for r in recipes if all(n in st.session_state.my_pantry for n in r['needs'])]
    
    if available:
        for r in available:
            with st.expander(f"✅ {r['name']}", expanded=False):
                st.write(f"**How to cook:** {r['steps']}")
    else:
        st.info("No 100% matches. Use the 'Search' mode to see what ingredients you are missing.")

else:
    st.subheader("🔍 Search Recipe")
    search = st.text_input("Enter dish name:", placeholder="e.g. Poha").strip().lower()
    if search:
        results = [r for r in recipes if search in r['name'].lower()]
        for r in results:
            missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
            with st.expander(f"📖 {r['name']}", expanded=True):
                st.write(f"**Steps:** {r['steps']}")
                if not missing:
                    st.success("✅ You have everything!")
                else:
                    st.warning(f"⚠️ Missing: {', '.join(missing)}")
                    if st.button(f"🛒 Add missing to Shopping List", key=f"shop_{r['name']}"):
                        for m in missing:
                            if m not in st.session_state.shopping_list:
                                st.session_state.shopping_list.append(m)
                        st.rerun()

# --- 8. SHOPPING LIST & WHATSAPP (Always at bottom) ---
# Remove items from shopping list if they were added back to pantry
st.session_state.shopping_list = [i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry]

if st.session_state.shopping_list:
    st.divider()
    st.subheader("🛒 Shopping List")
    for s_item in sorted(st.session_state.shopping_list):
        st.write(f"- {s_item}")
    
    # WhatsApp - Big Green Button
    msg = "🛒 *Kitchen List:* " + ", ".join(st.session_state.shopping_list)
    wa_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    
    st.markdown(f'''
    <a href="{wa_url}" target="_blank" style="text-decoration:none;">
        <div style="background-color:#25D366;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;font-size:1.1em;box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            📲 Share Shopping List via WhatsApp
        </div>
    </a>
    ''', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Shopping List"):
        st.session_state.shopping_list = []
        st.rerun()
