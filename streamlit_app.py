import streamlit
import pandas as pd
import requests
import snowflake.connector
import urllib.error

streamlit.title("My Mom's New Healthy Diner")
streamlit.header("Breakfast favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard Boiled Free-Range Egg")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index("Fruit")
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruity Vice Advice!")

def Fruity_vice_response_fun(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  fruityvice_normalized = fruityvice_normalized.set_index("name")
  return streamlit.dataframe(fruityvice_normalized)

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit of choice")
  else:
    fruitvice_normalized=Fruity_vice_response_fun(fruit_choice)
    streamlit.write('The user entered ', fruit_choice)
    
    
except urllib.error.URLError as e:
  streamlit.error()
    
def insert_value(value):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('" + "Jackfruit","papaya","kiwi" and "guava" +"')",value)
    streamlit.write('Thank you for adding  ', value)
    
  

def snowflake_querry():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()
    
if streamlit.button("Get Fruit List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = snowflake_querry()
  streamlit.text("FRUIT LOAD LIST CONTAINS :")
  streamlit.dataframe(my_cur)
fruit_to_add = streamlit.text_input('Which fruit would you like add?')
if streamlit.button("Add the fruit to list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  insert_value(fruit_to_add)

