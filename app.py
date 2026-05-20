import streamlit as st
import re

# ---------- PAGE ----------
st.set_page_config(
    page_title="Recipe Scaler",
    page_icon="🥣",
    layout="centered"
)

# ---------- STYLE ----------
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
background:
linear-gradient(
135deg,
#09090B,
#111827,
#1F2937
);
}

.block-container{
max-width:750px;
padding-top:2rem;
}

.big-title{
font-size:42px;
font-weight:800;
text-align:center;

background:linear-gradient(90deg,#D4AF37,#FFE88C);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.subtitle{
text-align:center;
color:#A5ACB8;
margin-bottom:20px;
}

.card{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:18px;
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,0.08);
box-shadow:0 8px 32px rgba(0,0,0,0.35);
}

.result-card{
background:#1F2937;
padding:16px;
border-radius:14px;
margin-bottom:10px;
border-left:4px solid #D4AF37;
transition:0.25s;
box-shadow:0 8px 32px rgba(0,0,0,0.35);
}

.result-card:hover{
transform:translateY(-2px);
}

.stButton button{
width:100%;
height:55px;
border-radius:16px;
font-size:18px;
font-weight:700;
background:linear-gradient(90deg,#D4AF37,#F3D36B);
color:black;
border:none;
transition:0.25s;
}

.stButton button:hover{
transform:scale(1.02);
}

.stTextArea textarea{
border-radius:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "result" not in st.session_state:
    st.session_state.result = None

if "saved_recipes" not in st.session_state:
    st.session_state.saved_recipes = {}

# ---------- PARSE ----------
def parse_recipe(text):
    data = []

    for line in text.split("\n"):
        match = re.match(r"(.+?)\s+([\d.]+)", line.strip())

        if match:
            data.append({
                "name": match.group(1),
                "amount": float(match.group(2))
            })

    return data

# ---------- SCALE CORE ----------
def scale_recipe(recipe, factor, locked=None):
    result = []

    for x in recipe:

        if locked and x["name"] in locked:
            scaled = x["amount"]
        else:
            scaled = x["amount"] * factor

        result.append({
            "name": x["name"],
            "scaled": round(scaled, 2)
        })

    return result

# ---------- TITLE ----------
st.markdown('<div class="big-title">🥣 Recipe Scaler</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pro Kitchen Tool</div>', unsafe_allow_html=True)

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Рецепт", "⚙ Настройки", "📊 Результат", "📚 Сохранённые"]
)

# ---------- TAB 1 ----------
with tab1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    recipe = st.text_area(
        "Рецепт",
        height=200,
        placeholder="Мука 1000\nВода 620\nСоль 20"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- TAB 2 ----------
with tab2:

    if recipe:

        data = parse_recipe(recipe)

        names = [x["name"] for x in data]

        mode = st.radio(
            "Режим",
            ["По ингредиенту", "По общему весу", "По порциям"]
        )

        locked = st.multiselect("Зафиксировать ингредиенты", names)

        factor = 1.0

        if mode == "По ингредиенту":

            base = st.selectbox("База", names)
            value = st.number_input("Значение", value=1000.0)

            base_amount = next(x["amount"] for x in data if x["name"] == base)
            factor = value / base_amount

        elif mode == "По общему весу":

            total = sum(x["amount"] for x in data)
            value = st.number_input("Новый общий вес", value=2000.0)
            factor = value / total

        elif mode == "По порциям":

            servings = st.number_input("Порции", value=10.0)
            factor = servings / 10

        if st.button("Пересчитать"):

            st.session_state.result = scale_recipe(
                data,
                factor,
                locked
            )

        # ---------- SAVE BLOCK ----------
        st.markdown("---")

        recipe_name = st.text_input("Название рецепта")

        if st.button("💾 Сохранить рецепт"):

            if recipe_name and st.session_state.result:

                st.session_state.saved_recipes[recipe_name] = {
                    "recipe_text": recipe,
                    "result": st.session_state.result,
                    "factor": factor
                }

                st.success("Рецепт сохранён")

            else:
                st.warning("Сначала введи название и пересчитай рецепт")

# ---------- TAB 3 ----------
with tab3:

    if st.session_state.result:

        st.markdown("### Результат")

        for x in st.session_state.result:

            st.markdown(
                f"""
                <div class="result-card">
                <b>{x['name']}</b><br>
                {x['scaled']}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("Сначала введи рецепт и нажми пересчитать")

# ---------- TAB 4 ----------
with tab4:

    st.markdown("### 📚 Сохранённые рецепты")

    if st.session_state.saved_recipes:

        for name, data in st.session_state.saved_recipes.items():

            st.markdown(f"### {name}")

            st.code(data["recipe_text"])

            if st.button(f"📂 Загрузить {name}"):

                st.session_state.result = data["result"]

                st.success("Рецепт загружен в результат")

    else:
        st.info("Пока нет сохранённых рецептов")