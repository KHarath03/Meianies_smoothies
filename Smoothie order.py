
# Import python packages.
import streamlit as st 

from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

session = get_active_session()
st.title("Customize your smoothie:")
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
   
    for  fruit_chosen in ingradients_list:
        ingradients_string += fruit_chosen + ' '
# st.write(ingradients_string)
    time_to_insert =st.button("Submit Order")
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
                    values ('""" + ingradients_string + """' , '""" + order_name + """')"""

    #st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success(f" {order_name} Your Smoothie is ordered!'.", icon="✅")

        
