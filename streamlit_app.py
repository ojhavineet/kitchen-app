import streamlit as st
import urllib.parse

# --- 1. App Config ---
st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="chef_icon.png", layout="centered")

# --- 2. State Management ---
if 'my_pantry' not in st.session_state:
    # Starting with a few basics for Pune households
    st.session_state.my_pantry = set(["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato", "Ginger", "Garlic"])
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = set()

# --- 3. Full Recipe Database ---
recipes = [
    {"name": "Quick Masala Poha", "cuisine": "Quick & Tired", "needs": ["Poha (Thick)", "Onion", "Green Chili"], "steps": "Wash poha. Sauté onions/chilies. Steam 2 mins."},
    {"name": "Vangi Bhaji", "cuisine": "Maharashtrian", "needs": ["Brinjal", "Onion", "Goda Masala"], "steps": "Sauté onions and brinjal with Goda Masala."},
    {"name": "Pithla", "cuisine": "Maharashtrian", "needs": ["Besan", "Onion", "Garlic"], "steps": "Make besan slurry. Sauté garlic/onions. Cook until thick."},
    {"name": "Sabudana Khichdi", "cuisine": "Maharashtrian", "needs": ["Sabudana", "Potato", "Green Chili"], "steps": "Sauté soaked sabudana with potatoes. Skip peanuts for Dviti."},
    {"name": "Moong Dal Paratha", "cuisine": "Lunchbox", "needs": ["Atta", "Moong Dal", "Ghee"], "steps": "Stuff paratha with cooked dal and fry with ghee."},
    {"name": "Schezwan Paneer", "cuisine": "Chinese", "needs": ["Paneer", "Schezwan Sauce", "Capsicum"], "steps": "Sauté capsicum. Add sauce and paneer cubes."}
]

# --- 4. Main UI Header ---
col1, col2 = st.columns([1, 5])
with col1: st.image("chef_icon.png", width=70)
with col2: st.title("Punekar Kitchen Pro")

st.write("---")

# --- 5. DUAL MODE TOGGLE ---
view_mode = st.radio("How would you like to decide?", ["Suggest based on my ingredients", "Search for a specific dish"], horizontal=True)

if view_mode == "Suggest based on my ingredients":
    st.subheader("👨‍🍳 Ready to Cook Now")
    # Only show recipes where 'needs' is a subset of 'my_pantry'
    ready_recipes = [r for r in recipes if set(r['needs']).issubset(st.session_state.my_pantry)]
    
    if ready_recipes:
        for r in ready_recipes:
            with st.expander(f"✅ {r['name']} ({r['cuisine']})", expanded=False):
                st.write(f"**Instructions:** {r['steps']}")
                st.info(f"Ingredients used: {', '.join(r['needs'])}")
    else:
        st.warning("No recipes match 100% of your current stock. Try the 'Search' mode to see what you need to buy!")

else:
    st.subheader("🔍 Search for a Dish")
    search_query = st.text_input("What are you craving?", placeholder="e.g. Paneer, Poha...").strip().lower()
    
    if search_query:
        results = [r for r in recipes if search_query in r['name'].lower()]
        if results:
            for r in results:
                missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
                with st.expander(f"📖 {r['name']}", expanded=True):
                    if not missing:
                        st.success("✅ Everything available!")
                        st.write(f"**Steps:** {r['steps']}")
                    else:
                        st.warning(f"⚠️ Missing: {', '.join(missing)}")
                        if st.button(f"➕ Add missing for {r['name']} to Shopping List"):
                            for i in missing: st.session_state.shopping_list.add(i)
                            st.toast("List updated!")
        else:
            st.error("Not found in our recipe book.")

# --- 6. Smart Shopping List (Same as before) ---
if st.session_state.shopping_list:
    # Auto-cleanup: if she adds an item to pantry, it leaves the shopping list
    st.session_state.shopping_list = {i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry}
    
    if st.session_state.shopping_list:
        st.divider()
        st.subheader("🛒 Shopping List")
        items_text = "\n".join([f"- {i}" for i in sorted(st.session_state.shopping_list)])
        st.info(items_text)
        
        msg = f"🛒 *Kitchen List:*\n{items_text}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f'''<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366;color:white;padding:12px;border-radius:10px;text-align:center;font-weight:bold;">
                📲 WhatsApp List to Anyone
            </div></a>''', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Shopping List"):
            st.session_state.shopping_list = set()
            st.rerun()

# --- 7. Sidebar Pantry ---
with st.sidebar:
    st.header("📦 Inventory")
    with st.expander("Update Stock"):
        new_item = st.text_input("Add item:")
        if st.button("Add"):
            st.session_state.my_pantry.add(new_item)
            st.rerun()
        st.write("---")
        st.write(f"Current Stock: {', '.join(sorted(st.session_state.my_pantry))}")
