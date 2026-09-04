# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f"Customize your smoothie!")

name_on_order = st.text_input("Name on the order")

st.write('The name on your Smoothie order will be:', name_on_order)

fruit_options = session.table("smoothies.test.fruit_options").select(col("FRUIT_NAME"))

options = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if options:
    fruits_list = ''

    for fruit in options:
        fruits_list += fruit + ' '
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit}")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    st.write("You selected:", fruits_list)
    
    button = st.button("Submit order!")
    
    if button:
        session.sql(
        "INSERT INTO smoothies.test.orders (name_on_order, ingredients) VALUES (?, ?)",
        params=[name_on_order, fruits_list]
    ).collect()
        
        st.success(f'Order submitted, {name_on_order}!', icon="✅")
