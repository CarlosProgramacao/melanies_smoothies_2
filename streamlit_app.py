# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
session = get_active_session()

# Write directly to the app
st.title(f"Customize your smoothie!")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

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

    st.write("You selected:", fruits_list)
    
    button = st.button("Submit order!")
    
    if button:
        session.sql(
        "INSERT INTO smoothies.test.orders (name_on_order, ingredients) VALUES (?, ?)",
        params=[name_on_order, fruits_list]
    ).collect()
        
        st.success(f'Order submitted, {name_on_order}!', icon="✅")
