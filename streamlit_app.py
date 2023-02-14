import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healty Diner')

streamlit.header('My Mom\'s New Healthy Diner')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{this_fruit_choice}")
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get more information.")
    else:
        df = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(df)
except:
    streamlit.error()


def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()


streamlit.header("The fruit list contains:")
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

def insert_fruit(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"INSERT INTO pc_rivery_db.public.fruit_load_list VALUES ('{new_fruit}')")
        return f"Thanks for adding {new_fruit}"

streamlit.header("View Our Fruit List - Add Your Favorites!")
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    message = insert_fruit(add_my_fruit)
    my_cnx.close()
    streamlit.text(message)

## Google Forms ID - 1A1enbY2g41lY2h4NoWySNVyXwLR0WJxd0-2i_O3LYUQ
## FoodData Central API key - eLgugHDaVGeho9PHdfhOaDj6XyI5bZujsZAszSih
