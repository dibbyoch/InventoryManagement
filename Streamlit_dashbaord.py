import streamlit as st
import pandas as pd
import json
import sqlite3
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
if st.button("Check Inventory"):
    st.table(pd.DataFrame(inventory_table, columns=["Product ID", "Name", "Price", "Product Code", "Quantity"]))

# User inputs for the purchase
userinput_productid = st.text_input("Enter Product ID:")
userinput_quantity = st.number_input("Enter Quantity:", min_value=1, step=1)
Userinput_name = st.text_input("Enter your Name:")
Userinput_number = st.text_input("Enter your Mobile Number:")
Userinput_country = st.text_input("Enter your Country:")

# Button to submit purchase
if st.button("Submit Purchase"):
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


st.markdown("""
    <style>
    .rainbow-button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        color: white;
        background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-position 1s ease;
        background-size: 400%;
    }
    
    .rainbow-button:hover {
        background-position: 1000%;
    }
    
    .rainbow-button-container {
        text-align: center;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# Button with the rainbow effect
button_html = """
<div class="rainbow-button-container">
    <form action="#">
        <input type="submit" class="rainbow-button" value="Show Sales Data"/>
    </form>
</div>
"""

# Render the rainbow button and check for interaction
st.markdown(button_html, unsafe_allow_html=True)

if st.form_submit_button("Show Sales Data"):
    display_sql_table()
if st.button("Clear sales table"):
    clear_sales_records()
