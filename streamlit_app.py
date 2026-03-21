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

# --- 3. Detailed Recipe Database ---
recipes = [
    {
        "name": "Quick Masala Poha", 
        "needs": ["Poha (Thick)", "Onion", "Green Chili", "Turmeric"], 
        "steps": "1. Wash Poha and set aside. 2. Sauté onions, green chilies, and curry leaves in oil. 3. Add turmeric and salt. 4. Mix in Poha, cover and steam for 2 mins. Garnish with coriander.",
        "cuisine": "Quick & Tired"
    },
    {
        "name": "Vangi Bhaji (Brinjal)", 
        "needs": ["Brinjal", "Onion", "Goda Masala", "Ginger", "Garlic"], 
        "steps": "1. Slice Brinjal. 2. Heat oil, sauté onions, ginger, and garlic paste. 3. Add Goda Masala and red chili powder. 4. Add brinjal and a splash of water. Cover and cook until tender.",
        "cuisine": "Maharashtrian"
    },
    {
        "name": "Pithla", 
        "needs": ["Besan", "Onion", "Garlic", "Green Chili"], 
        "steps": "1. Make a smooth slurry of Besan and water. 2. Sauté crushed garlic, green chilies, and onions. 3. Pour in the slurry while stirring continuously to avoid lumps. 4. Cook until thick and garnish with coriander.",
        "cuisine": "Maharashtrian"
    },
    {
        "name": "Sabudana Khichdi", 
        "needs": ["Sabudana", "Potato", "Green Chili", "Cumin Seeds"], 
        "steps": "1. Soak Sabudana overnight. 2. Sauté cumin seeds and diced potatoes in oil/ghee. 3. Add green chilies and soaked sabudana. 4. Cook until translucent. (Note: Peanuts skipped for Dviti's safety).",
        "cuisine": "Maharashtrian"
    },
    {
        "name": "Schezwan Paneer", 
        "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion", "Garlic"], 
        "steps": "1. Cube the paneer and sauté until lightly brown. 2. In the same pan, sauté garlic, sliced onions, and capsicum. 3. Add Schezwan sauce and toss the paneer back in. 4. Serve hot.",
        "cuisine": "Chinese"
    },
    {
        "name": "Moong Dal Paratha", 
        "needs": ["Atta", "Moong Dal", "Ghee", "Turmeric"], 
        "steps": "1. Pressure cook Moong Dal with turmeric until dry. 2. Mash the dal with salt and chilies. 3. Stuff a small ball of dal into Atta dough. 4. Roll out and roast on a tawa with Ghee until golden.",
        "cuisine": "Lunchbox Idea"
    },
    {
        "name": "Misal Pav",
        "needs": ["Matki", "Onion", "Tomato", "Kanda Lasun Masala", "Pav"],
        "steps": "1. Sprout the Matki. 2. Make a spicy 'kat' using onions, tomatoes, and Kanda Lasun Masala. 3. Add Matki and simmer. 4. Serve with Pav and farsan.",
        "cuisine": "Maharashtrian"
    }
]

# --- 4. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato", "Ginger", "Garlic"])
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = set()
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- 5. Main UI Header ---
col1, col2 = st.columns([1, 5])
with col1:
    try: st.image("chef_icon.png", width=70)
    except: st.write("🍳")
with col2: st.title("Punekar Kitchen Pro")

# --- 6. Sidebar: Inventory Management ---
with st.sidebar:
    st.header("📦 Inventory Management")
    with st.expander("➕ Add Stock", expanded=True):
        cat = st.selectbox("Choose Category:", list(CATEGORIES.keys()))
        selected = st.multiselect(f"Select {cat}:", CATEGORIES[cat])
        if st.button("Add to Kitchen"):
            for item in selected: st.session_state.my_pantry.add(item)
            st.rerun()
    
    st.divider()
    st.subheader("🛒 Current Stock")
    st.write(", ".join(sorted(st.session_state.my_pantry)))
    if st.button("🗑️ Reset Pantry"):
        st.session_state.my_pantry = set(["Salt", "Turmeric", "Ginger", "Garlic"])
        st.rerun()

# --- 7. Main Logic (Search & Suggest) ---
st.divider()
view_mode = st.radio("What's the plan?", ["Suggest based on ingredients", "Search for a dish"], horizontal=True)

if view_mode == "Suggest based on ingredients":
    st.subheader("👨‍🍳 Ready to Cook Now")
    ready = [r for r in recipes if set(r['needs']).issubset(st.session_state.my_pantry)]
    if ready:
        for r in ready:
            rating = st.session_state.ratings.get(r['name'], "Not rated yet")
            with st.expander(f"✅ Ready: {r['name']} ({rating})", expanded=False):
                st.write(f"**Instructions:** {r['steps']}")
                # Rating Input
                new_rating = st.select_slider(f"Rate {r['name']}:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=r['name'])
                if st.button(f"Save Rating", key=f"btn_{r['name']}"):
                    st.session_state.ratings[r['name']] = new_rating
                    st.rerun()
    else:
        st.info("Nothing is 100% ready. Switch to 'Search' to see what to buy!")

else:
    st.subheader("🔍 Search for a Dish")
    query = st.text_input("Type here...", placeholder="Poha, Paneer, Misal...").strip().lower()
    if query:
        results = [r for r in recipes if query in r['name'].lower()]
        for r in results:
            missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
            rating = st.session_state.ratings.get(r['name'], "Not rated yet")
            with st.expander(f"📖 {r['name']} ({rating})", expanded=True):
                st.write(f"**Detailed Recipe:** {r['steps']}")
                if not missing: st.success("✅ All ingredients available!")
                else:
                    st.warning(f"⚠️ Missing: {', '.join(missing)}")
                    if st.button(f"Add missing items to Shopping List", key=r['name']):
                        for i in missing: st.session_state.shopping_list.add(i)
                        st.toast("Updated!")

# --- 8. Shopping List ---
if st.session_state.shopping_list:
    st.session_state.shopping_list = {i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry}
    if st.session_state.shopping_list:
        st.divider()
        st.subheader("🛒 Shopping List")
        items_list = sorted(list(st.session_state.shopping_list))
        st.info("\n".join([f"- {i}" for i in items_list]))
        
        msg = f"🛒 *Kitchen List:* " + ", ".join(items_list)
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f'''<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366;color:white;padding:12px;border-radius:10px;text-align:center;font-weight:bold;">📲 WhatsApp List</div></a>''', unsafe_allow_html=True)
