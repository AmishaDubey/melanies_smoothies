import streamlit as st
import requests

from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")

st.write("Choose the fruits you want in your custom Smoothie!")

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Customer name
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write(f"The name on your Smoothie will be: {name_on_order}")

# Fruit options from Snowflake
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Build insert statement
my_insert_stmt = None

if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS
    (INGREDIENTS, NAME_ON_ORDER)
    VALUES
    ('{ingredients_string}', '{name_on_order}')
    """

# Submit order
if st.button("Submit Order"):

    if my_insert_stmt:
        session.sql(my_insert_stmt).collect()
        st.success("✅ Your Smoothie is ordered!")
    else:
        st.warning("Please select at least one ingredient.")

# Fruit API section
st.subheader("Fruit Nutrition Information")

fruit_choice = st.selectbox(
    "Choose a fruit",
    ["watermelon"]
)

if fruit_choice:

    smoothiefroot_response = requests.get(
        f"https://my.smoothiefroot.com/api/fruit/{fruit_choice}"
    )

    if smoothiefroot_response.status_code == 200:
        st.json(smoothiefroot_response.json())
    else:
        st.error("Could not retrieve fruit information.")
