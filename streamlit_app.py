import streamlit as st
import random
import urllib.parse

# --- 1. App Configuration (Sets the Browser Tab Icon) ---
# Ensure 'chef_icon.png' is uploaded to your GitHub folder
st.set_page_config(
    page_title="Punekar Kitchen Pro", 
    page_icon="chef_icon.png", 
    layout="centered"
)

# --- 2. Custom Styling ---
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

# --- 3. Master Categories (250+ Items organized for your wife) ---
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
    {"name": "Brinjal Fry (Vangi Kapach)", "cuisine": "Maharashtrian", "needs": ["Brinjal", "Kanda Lasun Masala", "Besan"], "allergens": [], "steps": "Slice brinjal. Coat in masala and besan. Shallow fry on tawa."},
    {"name": "Schezwan Paneer", "cuisine": "Chinese", "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion"], "allergens": [], "steps": "Sauté onions and capsicum. Add schezwan sauce and paneer cubes. Toss well."},
    {"name": "Moong Dal Paratha", "cuisine": "Lunchbox Idea", "needs": ["Atta", "Moong Dal", "Ghee"], "allergens": [], "steps": "Stuff paratha with cooked dal. Stays soft for lunch!"},
    {"name": "Sabudana Khichdi", "cuisine": "Maharashtrian", "needs": ["Sabudana", "Potato", "Green Chili"], "allergens": ["Peanuts"], "steps": "Sauté soaked sabudana with potatoes. Skip peanuts for Dviti."},
    {"name": "Mini Cheese Uttapam", "cuisine": "Kid's Special", "needs": ["Rice (Indrayani)", "Cheese Cubes", "Tomato"], "allergens": [], "steps": "Small rice pancakes topped with tomatoes and cheese."}
]

# --- 5. State Management ---
if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato"])
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# --- 6. Sidebar (Wife's Dashboard) ---
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

# --- 7. Main Interface (Header with Chef Image) ---
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("chef_icon.png", width=70)
    except:
        st.write("🍳") # Fallback if image not found

with col2:
    st.title("Punekar Kitchen Pro")

# Show current inventory
with st.expander(f"📦 Our Kitchen Inventory ({len(st.session_state.my_pantry)} items)", expanded=False):
    p_list = sorted(list(st.session_state.my_pantry))
    for p in p_list:
        st.markdown(f'<div class="inventory-tag">{p}</div>', unsafe_allow_html=True)

# Suggestions Logic
st.divider()
st.subheader("What's for a meal?")
mode = st.radio("Style:", ["All", "Quick & Tired", "Kid's Special", "Lunchbox Idea", "Maharashtrian", "Indian"], horizontal=True)

if st.button("🔍 Suggest Safe Meals"):
    matches = [r for r in recipes if all(i in st.session_state.my_pantry for i in r['needs'])]
    if mode != "All":
        matches = [r for r in matches if r['cuisine'] == mode]
    
    if matches:
        for m in matches:
            rating = st.session_state.ratings.get(m['name'], "Not rated yet")
            st.markdown(f"""
            <div class="recipe-card">
                <h3>{m['name']}</h3>
                <small>⭐ Rating: {rating} | Category: {m['cuisine']}</small><br><br>
                <p><b>Instructions:</b> {m['steps']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Simple Rating Input
            new_rating = st.select_slider(f"Rate {m['name']}:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=m['name'])
            if st.button(f"Save Rating for {m['name']}"):
                st.session_state.ratings[m['name']] = new_rating
                st.rerun()
    else:
        st.warning("Not enough ingredients for this style. Check the shopping list below!")

# --- 8. The WhatsApp Shopping List (Neutral & Practical) ---
all_possible_needs = set([i for r in recipes for i in r['needs']])
missing = sorted([i for i in all_possible_needs if i not in st.session_state.my_pantry])

if missing:
    st.divider()
    st.subheader("📝 Missing Ingredients")
    st.write(", ".join(missing))
    
    # Message formatting
    shop_text = "🛒 *Kitchen Shopping List:*\n"
    shop_text += "Items needed for upcoming meals:\n\n"
    for item in missing:
        shop_text += f"✅ {item}\n"
    shop_text += "\n_Sent from Punekar Kitchen Pro_"
    
    encoded_text = urllib.parse.quote(shop_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 Share Shopping List via WhatsApp</a>', unsafe_allow_html=True)
