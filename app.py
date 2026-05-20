import streamlit as st
import re

st.set_page_config(
    page_title="Recipe Scaler",
    page_icon="🥣",
    layout="centered"
)

# ---------- STYLE ----------

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:2rem;
max-width:700px;
}

.stApp{

background:
linear-gradient(
135deg,
#0F172A,
#111827,
#1E293B
);

}

.big-title{

font-size:42px;

font-weight:800;

text-align:center;

margin-bottom:10px;

background:
linear-gradient(
90deg,
#D4AF37,
#F6E27A
);

-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

}

.subtitle{

text-align:center;

color:#B8BCC8;

margin-bottom:25px;

}

.glass{

background:
rgba(
255,
255,
255,
0.05
);

padding:20px;

border-radius:20px;

backdrop-filter:blur(12px);

border:
1px solid rgba(
255,
255,
255,
0.08
);

margin-bottom:15px;

}

.result-card{

background:
linear-gradient(
135deg,
#1F2937,
#111827
);

padding:15px;

border-radius:16px;

margin-bottom:10px;

border-left:
5px solid #D4AF37;

}

.stButton button{

width:100%;

height:55px;

font-size:18px;

font-weight:700;

border-radius:16px;

background:
linear-gradient(
90deg,
#D4AF37,
#C39A22
);

color:black;

border:none;

}

.stButton button:hover{

background:
linear-gradient(
90deg,
#E8C860,
#D4AF37
);

}

</style>
""", unsafe_allow_html=True)

# ---------- PARSE ----------

def parse_recipe(text):

    ingredients=[]

    for line in text.split("\n"):

        match=re.match(
            r"(.+?)\s+([\d.]+)",
            line.strip()
        )

        if match:

            ingredients.append({

                "name":
                match.group(1),

                "amount":
                float(
                match.group(2)
                )

            })

    return ingredients

# ---------- SCALE ----------

def scale_recipe(
ingredients,
base,
new_value
):

    original=next(

    x["amount"]

    for x in ingredients

    if x["name"]==base

    )

    factor=new_value/original

    result=[]

    for x in ingredients:

        result.append({

        "name":
        x["name"],

        "scaled":
        round(
        x["amount"]*
        factor,
        2
        )

        })

    return result

# ---------- UI ----------

st.markdown(
'<div class="big-title">🥣 Recipe Scaler</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">AI Recipe Scaling Tool</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="glass">',
unsafe_allow_html=True
)

recipe=st.text_area(
"Рецепт",
height=180,
placeholder=
"""Мука 1000
Вода 620
Соль 20"""
)

st.markdown(
"</div>",
unsafe_allow_html=True
)

if recipe:

    data=parse_recipe(recipe)

    if data:

        base=st.selectbox(

        "Основа",

        [

        x["name"]

        for x in data

        ]

        )

        value=st.number_input(
        "Новое значение",
        value=1000.0
        )

        if st.button(
        "Пересчитать"
        ):

            result=scale_recipe(
            data,
            base,
            value
            )

            st.markdown(
            "### Результат"
            )

            for x in result:

                st.markdown(

                f"""

<div class="result-card">

<b>

{x["name"]}

</b>

<br>

{x["scaled"]}

</div>

""",

unsafe_allow_html=True

)