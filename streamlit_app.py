import streamlit as st
import urllib.parse

st.set_page_config(page_title="Punekar Kitchen Pro", page_icon="chef_icon.png", layout="centered")

CATEGORIES = {
    "🥦 Veggies": ["Onion", "Tomato", "Potato", "Ginger", "Garlic", "Green Chili", "Coriander", "Curry Leaves", "Lemon", "Cauliflower", "Cabbage", "Capsicum", "Carrot", "French Beans", "Brinjal", "Okra (Bhindi)", "Bottle Gourd", "Ridge Gourd", "Bitter Gourd", "Pumpkin", "Drumstick", "Spring Onion", "Sweet Potato", "Mint", "Spinach", "Methi", "Radish", "Cucumber", "Beetroot", "Corn", "Mushroom", "Broccoli", "Colocasia Leaves", "Ivy Gourd (Tondli)"],
    "🌾 Grains/Flours": ["Atta", "Rice (Basmati)", "Rice (Indrayani)", "Poha (Thick)", "Poha (Thin)", "Besan", "Maida", "Rava (Suji)", "Jowar Flour", "Bajra Flour", "Nachni Flour", "Sabudana", "Corn Flour", "Vermicelli", "Oats"],
    "🥣 Dals/Pulses": ["Tur Dal", "Moong Dal", "Chana Dal", "Urad Dal", "Masoor Dal", "Matki", "Kabuli Chana", "Kala Chana", "Rajma", "Green Moong", "Chowli"],
    "🥛 Dairy/Cold": ["Milk", "Curd", "Paneer", "Butter", "Ghee", "Cheese Slices", "Cheese Cubes", "Fresh Cream", "Buttermilk"],
    "🥫 Sauces/Pantry": ["Tomato Ketchup", "Soy Sauce", "Green Chili Sauce", "Red Chili Sauce", "Vinegar", "Schezwan Sauce", "Pasta Sauce", "Mayonnaise", "Honey", "Jaggery", "Sugar", "Tea", "Coffee", "Bournvita", "Jam", "Pickle"],
    "🧂 Spices": ["Salt", "Turmeric", "Red Chili Powder", "Coriander Powder", "Cumin Seeds", "Mustard Seeds", "Hing", "Kanda Lasun Masala", "Goda Masala", "Garam Masala", "Kasuri Methi", "Ajwain", "Black Pepper", "Chat Masala", "Sambhar Powder", "Pav Bhaji Masala"],
    "🥜 Nuts/Dry Fruits": ["Sesame Seeds (Til)", "Sunflower Seeds", "Dates", "Coconut (dry)", "Coconut (fresh)"],
    "🧼 Cleaning/Utility": ["Dishwash Soap", "Handwash", "Detergent", "Floor Cleaner", "Garbage Bags", "Kitchen Rolls", "Foil"]
}

# ALLERGY LIST — Peanuts, Cashews, Almonds, Walnuts, Eggs, Seafood are permanently excluded
DVITI_ALLERGIES = ["Peanuts", "Cashews", "Almonds", "Walnuts", "Pistachios", "Eggs", "Fish", "Prawns", "Seafood"]

recipes = [
    {
        "name": "Quick Masala Poha",
        "cuisine": "Quick & Tired",
        "needs": ["Poha (Thick)", "Onion", "Green Chili", "Turmeric"],
        "allergens": [],
        "steps": "1. Wash Poha under water and drain. 2. Heat oil, add mustard seeds, curry leaves. 3. Add onions and green chili, sauté till golden. 4. Add turmeric and salt. 5. Mix in Poha, cover and steam for 2 mins. Garnish with coriander and lemon."
    },
    {
        "name": "Vangi Bhaji",
        "cuisine": "Maharashtrian",
        "needs": ["Brinjal", "Onion", "Goda Masala", "Turmeric"],
        "allergens": [],
        "steps": "1. Slice Brinjal into roundels and keep in water. 2. Heat oil, sauté onions until golden. 3. Add Goda Masala, turmeric, red chili powder. 4. Drain brinjal and add to pan. 5. Sprinkle a little water, cover and cook 10 mins until soft."
    },
    {
        "name": "Pithla",
        "cuisine": "Maharashtrian",
        "needs": ["Besan", "Onion", "Garlic", "Green Chili"],
        "allergens": [],
        "steps": "1. Make smooth slurry of Besan with 2 cups water, add salt and turmeric. 2. Heat oil, add mustard seeds and hing. 3. Sauté crushed garlic and green chili. 4. Add onions and sauté. 5. Pour in slurry, stir continuously on medium flame until thick. Serve with Bhakri."
    },
    {
        "name": "Sabudana Khichdi",
        "cuisine": "Maharashtrian",
        "needs": ["Sabudana", "Potato", "Green Chili", "Cumin Seeds", "Ghee"],
        "allergens": ["Peanuts"],
        "steps": "1. Soak Sabudana 4-6 hours or overnight. 2. Heat ghee, add cumin seeds. 3. Add diced boiled potato and green chili. 4. Add soaked sabudana, salt, and mix. 5. Cook on low flame until translucent. Note: Peanuts skipped — safe for Dviti. Add Sesame seeds for crunch instead."
    },
    {
        "name": "Schezwan Paneer",
        "cuisine": "Chinese",
        "needs": ["Paneer", "Schezwan Sauce", "Capsicum", "Onion"],
        "allergens": [],
        "steps": "1. Cut paneer into cubes. 2. Heat oil on high flame. 3. Sauté diced onion and capsicum for 2 mins. 4. Add Schezwan sauce and mix. 5. Add paneer, toss well for 2 mins. Serve immediately."
    },
    {
        "name": "Moong Dal Paratha",
        "cuisine": "Lunchbox Idea",
        "needs": ["Atta", "Moong Dal", "Ghee", "Turmeric"],
        "allergens": [],
        "steps": "1. Pressure cook Moong Dal with turmeric and salt until dry. 2. Mash well. 3. Take atta dough ball, flatten, stuff with dal filling. 4. Seal and roll gently. 5. Roast on tawa with ghee both sides until golden. Stays soft till lunch."
    },
    {
        "name": "Misal Pav",
        "cuisine": "Maharashtrian",
        "needs": ["Matki", "Onion", "Tomato", "Kanda Lasun Masala"],
        "allergens": [],
        "steps": "1. Sprout Matki 1-2 days ahead. 2. Pressure cook sprouts for 2 whistles. 3. Make spicy kat: sauté onion, tomato, Kanda Lasun Masala in oil. 4. Add sprouts and simmer 10 mins. 5. Serve topped with farsan, raw onion, and lemon."
    },
    {
        "name": "Cheese Chili Toast",
        "cuisine": "Quick & Tired",
        "needs": ["Bread (White)", "Cheese Slices", "Tomato Ketchup", "Green Chili"],
        "allergens": [],
        "steps": "1. Spread ketchup on bread slices. 2. Add finely chopped green chili. 3. Place cheese slice on top. 4. Toast on tawa on low flame with lid until cheese melts. 5. Ready in under 5 minutes!"
    },
    {
        "name": "Mini Paneer Tikka",
        "cuisine": "Kid's Special",
        "needs": ["Paneer", "Curd", "Turmeric", "Red Chili Powder"],
        "allergens": [],
        "steps": "1. Cube paneer. 2. Marinate in curd, turmeric, mild red chili powder, and salt for 15 mins. 3. Heat ghee on tawa. 4. Pan fry paneer on all sides until lightly golden. 5. Safe for Dviti — mild and no allergens."
    },
    {
        "name": "Moong Dal Khichdi",
        "cuisine": "Kid's Special",
        "needs": ["Rice (Basmati)", "Moong Dal", "Ghee", "Turmeric"],
        "allergens": [],
        "steps": "1. Wash rice and moong dal together. 2. Pressure cook with turmeric, salt, and 3 cups water for 3-4 whistles. 3. Open and mix well. 4. Add a generous spoon of ghee. 5. Soft, safe, and nutritious for Dviti."
    },
    {
        "name": "Veg Hakka Noodles",
        "cuisine": "Chinese",
        "needs": ["Vermicelli", "Capsicum", "Carrot", "Soy Sauce", "Vinegar"],
        "allergens": [],
        "steps": "1. Boil noodles al dente, drain, toss with oil. 2. Heat oil on high flame in a wok. 3. Add thinly sliced carrot and capsicum, stir fry 2 mins. 4. Add soy sauce, vinegar, salt, pepper. 5. Toss in noodles. Serve immediately."
    },
    {
        "name": "Tomato Dal",
        "cuisine": "Indian",
        "needs": ["Tur Dal", "Tomato", "Garlic", "Cumin Seeds", "Turmeric"],
        "allergens": [],
        "steps": "1. Pressure cook Tur Dal with turmeric for 3 whistles. 2. Heat oil, add cumin seeds and crushed garlic. 3. Add chopped tomato, cook till mushy. 4. Add red chili powder, salt. 5. Pour in cooked dal, mix and simmer 5 mins."
    }
]

if 'my_pantry' not in st.session_state:
    st.session_state.my_pantry = ["Salt", "Turmeric", "Cooking Oil", "Onion", "Tomato", "Ghee"]
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

with st.sidebar:
    st.header("📦 Manage Kitchen")

    with st.expander("➕ Add Items", expanded=True):
        cat = st.selectbox("Category:", list(CATEGORIES.keys()))
        selected = st.multiselect(f"Pick from {cat}:", CATEGORIES[cat])
        if st.button("Add to Pantry"):
            for item in selected:
                if item not in st.session_state.my_pantry:
                    st.session_state.my_pantry.append(item)
            st.rerun()

    st.subheader("📝 In Stock")
    for item in sorted(st.session_state.my_pantry):
        c1, c2 = st.columns([5, 1])
        c1.write(f"• {item}")
        if c2.button("X", key=f"del_sidebar_{item}"):
            st.session_state.my_pantry.remove(item)
            st.rerun()

    st.divider()
    if st.button("🗑️ Reset All"):
        st.session_state.my_pantry = ["Salt", "Turmeric"]
        st.rerun()

    st.divider()
    st.subheader("🛡️ Dviti's Safety")
    st.caption("App automatically blocks: Peanuts, Cashews, Almonds, Walnuts, Eggs, Seafood")

col1, col2 = st.columns([1, 5])
with col1:
    st.image("chef_icon.png", width=75)
with col2:
    st.title("Punekar Kitchen Pro")

st.divider()
tab1, tab2 = st.tabs(["💡 Suggest Meals", "🔍 Search Dish"])

with tab1:
    st.subheader("Ready to Cook (100% Match)")
    ready = [
        r for r in recipes
        if all(need in st.session_state.my_pantry for need in r['needs'])
        and not any(a in DVITI_ALLERGIES for a in r['allergens'])
    ]
    if ready:
        for r in ready:
            rating = st.session_state.ratings.get(r['name'], "Not rated yet")
            with st.expander(f"✅ {r['name']} — {r['cuisine']} ({rating})", expanded=False):
                st.write(r['steps'])
                new_rate = st.select_slider("Rate this meal:", options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], key=f"rate_{r['name']}")
                if st.button("Save Rating", key=f"btn_{r['name']}"):
                    st.session_state.ratings[r['name']] = new_rate
                    st.rerun()
    else:
        st.info("No 100% matches yet. Add more items to your pantry using the sidebar, or use the Search tab.")

with tab2:
    st.subheader("Look Up a Dish")
    query = st.text_input("What are you looking for?", placeholder="e.g. Poha, Paneer, Dal...").strip().lower()
    if query:
        results = [r for r in recipes if query in r['name'].lower()]
        if results:
            for r in results:
                missing = [i for i in r['needs'] if i not in st.session_state.my_pantry]
                allergy_alert = [a for a in r['allergens'] if a in DVITI_ALLERGIES]
                rating = st.session_state.ratings.get(r['name'], "Not rated yet")
                with st.expander(f"📖 {r['name']} — {r['cuisine']} ({rating})", expanded=True):
                    if allergy_alert:
                        st.error(f"⚠️ Contains allergen: {', '.join(allergy_alert)} — recipe modified for Dviti's safety. See steps.")
                    st.write(r['steps'])
                    if not missing:
                        st.success("✅ All ingredients available!")
                    else:
                        st.warning(f"Missing: {', '.join(missing)}")
                        if st.button(f"🛒 Add missing to Shopping List", key=f"add_shopp_{r['name']}"):
                            for m_item in missing:
                                if m_item not in st.session_state.shopping_list:
                                    st.session_state.shopping_list.append(m_item)
                            st.rerun()
        else:
            st.warning("Dish not found. Try another name.")

st.session_state.shopping_list = [i for i in st.session_state.shopping_list if i not in st.session_state.my_pantry]

if st.session_state.shopping_list:
    st.divider()
    st.subheader("📋 Your Shopping List")
    shop_items = sorted(st.session_state.shopping_list)
    for s_item in shop_items:
        st.write(f"- {s_item}")

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
