import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy dinner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 and Blueberry oatmeal')
streamlit.text('🥗 Kale, Spinach & rocket smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)



#create a repetable code bloack
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("please select a fruit to get information.")
   else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
        
         
         

except URLError as e:
  stremlit.error()









#dont run anything after here
#streamlit.stop()


streamlit.header("The fruit load list contains:")
#snowflake-related-functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from FRUIT_LOAD_LIST")
         return my_cur.fetchall()
    

# add button 

if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)

    
    


#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#= 
#my_cur.execute("Select * from fruit_load_list")
#my_data_rows = my_cur.fetchall()

#streamlit.dataframe(my_data_rows)

##streamlit.header("Fruityvice Fruit Advice!")
#fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
#streamlit.write('The user entered ', fruit_choice)




#my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
