import streamlit as st
import pandas as pd
import json
import sqlite3
import streamlit_extras

from ETL_process import display_sql_table,clear_sales_records
from inventory_management import process_purchase
#Function to load inventory data from JSON
fd = open("Records.json",'r')
js = fd.read()
fd.close()
records = json.loads(js)
#Load and display the current inventory using Streamlit
st.write("--------------- MENU ----------------")


#Create table to display inventory
inventory_table = []
for key, item in records.items():
    inventory_table.append([key, item['Name'], item['Price'], item['Product_ID'], item['Quantity']])

# Display inventory in table format

    # User inputs for the purchase
userinput_productid = st.text_input("Enter Product ID:")
userinput_quantity = st.number_input("Enter Quantity:", min_value=1, step=1)
Userinput_name = st.text_input("Enter your Name:")
Userinput_number = st.text_input("Enter your Mobile Number:")
Userinput_country = st.text_input("Enter your Country:")





# Define your custom CSS
button_styles = """
    <style>
    div.stButton:nth-of-type(1) button {  /* First button (Check Inventory) */
        background-color: #800080;
        color: white;
    }
    div.stButton:nth-of-type(2) button {  /* Second button (Submit Purchase) */
        background-color: #FF4500;
        color: white;
    }
    div.stButton:nth-of-type(3) button {  /* Third button (Show Sales Data) */
        background-color: #008CBA;
        color: white;
    }
    </style>
"""

# Inject custom styles
st.markdown(button_styles, unsafe_allow_html=True)

# Button examples with keys
if st.button("Check Inventory", key="check_inventory"):
    st.table(pd.DataFrame(inventory_table, columns=["Product ID", "Name", "Price", "Product Code", "Quantity"]))

if st.button("Submit Purchase", key="submit_purchase"):
    # Call process_purchase function
    result, transaction_id, billing_amount = process_purchase(
        userinput_productid, userinput_quantity, Userinput_name, Userinput_number, Userinput_country
    )

    # Handle result
    if result is True:
        st.success(f"Purchase Successful! Transaction ID: {transaction_id}")
        st.write(f"Total Amount: {billing_amount} Rupees")
    elif result is False:
        available_quantity = transaction_id  # Since product_quantity is returned in place of transaction_id when result is False
        st.error(f"Only {available_quantity} units are available for this product.")
        
        # Ask the user if they want to proceed with the available quantity
        proceed = st.radio("Would you like to proceed with the available quantity?", ('No', 'Yes'))
        
        if proceed == 'Yes':
            # Proceed with the available quantity
            result, transaction_id, billing_amount = process_purchase(
                userinput_productid, available_quantity, Userinput_name, Userinput_number, Userinput_country, proceed_with_max_quantity=True
            )
            
            if result is True:
                st.success(f"Purchase Successful with available quantity! Transaction ID: {transaction_id}")
                st.write(f"Total Amount: {billing_amount} Rupees")
            else:
                st.error(f"An error occurred while processing your purchase, because the is {transaction_id} products")
    else:
        st.error("Invalid Product ID")

if st.button("Show Sales Data", key="show_sales_data"):
    display_sql_table()


    
#if st.button("Clear Sales Data"):
    #clear_sales_records()
