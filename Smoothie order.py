
# Import python packages.
import streamlit as st 
from snowflake.snowpark.functions import col
import requests 

cnx =st.connection("snowflake")
session =cnx.session()

st.title("My Parents new healthy smoothie menu:")
st.write(""" Choose fruit in your Smoothie""")

order_name =st.text_input("Name your smoothie:")
st.write( "your Smoothie is called :",order_name )

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
  
ingradients_list =st.multiselect(
    'chose up to 5 ingradients :', my_dataframe, max_selections=5
    )

if ingradients_list:
    ingradients_string = ''
    for fruit_chosen in ingradients_list:
      ingradients_string += fruit_chosen + ' '
      st.subheader(fruit_chosen + 'Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)  
      sf_df = st.dataframe(data =smoothiefroot_response.json(), user_container_width= True)
 
      time_to_insert =st.button("Submit Order")
    
      my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
                    values ('""" + ingradients_string + """' , '""" + order_name + """')"""

      if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success(f" {order_name} Your Smoothie is ordered!'.", icon="✅")

        
