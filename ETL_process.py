#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#creating tables using SQLlite
import sqlite3
import json
import pandas as pd
def update_database():

    
    
    # Connect to SQLite database (or create it)
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            country TEXT
        )
    ''')
    
    # Create Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
            product_id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            engine TEXT,
            quantity INTEGER
        )
    ''')
    
    # Create Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            transaction_id TEXT PRIMARY KEY,
            user_id INTEGER,
            product_id TEXT,
            quantity INTEGER,
            billing_amount REAL,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (product_id) REFERENCES Items(product_id)
        )
    ''')
    
    conn.commit()
    
    
    #extracting data from the created JSON files
    import json
    
    with open('Records.json', 'r') as f:
        records = json.load(f)
    
    # Load sales.json
    with open('sales.json', 'r') as f:
        sales_data = json.load(f)
    
    # Insert data into the Items table
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    
    # Perform database operations
    
    
    for product_id, details in records.items():
        cursor.execute('''
            INSERT OR REPLACE INTO Items (product_id, name, price, engine, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, details['Name'], details['Price'], details['Engine'], int(details['Quantity'])))
        
    conn.commit()
    # Extract and transform sales data, and insert into Users and Sales tables
    
    conn = sqlite3.connect('inventory_management.db')
    cursor = conn.cursor()
    
    for transaction_id, sale in sales_data.items():
        # Insert user details into Users table (if not already present)
        cursor.execute('''
            INSERT OR IGNORE INTO Users (name, mobile, country)
            VALUES (?, ?, ?)
        ''', (sale['Name'], sale['Mobile'], sale['Country']))
        
        # Get the user_id for the inserted/ignored user
        cursor.execute('SELECT user_id FROM Users WHERE mobile = ?', (sale['Mobile'],))
        user_id = cursor.fetchone()[0]
    
        # Insert sales record into Sales table with the provided transaction_id
        cursor.execute('SELECT COUNT(*) FROM Sales WHERE transaction_id = ?', (transaction_id,))
        if cursor.fetchone()[0] == 0:  # If count is 0, the transaction_id does not exist
            # Insert sales record into Sales table with the provided transaction_id
            cursor.execute('''
                INSERT INTO Sales (transaction_id, user_id, product_id, quantity, billing_amount, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (transaction_id, user_id, sale['Product_ID'], sale['Quantity'], float(sale['Billing_Amount']), sale['Timestamp']))
        else:
            pass
    conn.commit()
    conn.close()
def display_sql_table():

    conn = sqlite3.connect('inventory_management.db')
    query = '''
        SELECT Users.user_id, Users.name, Users.mobile, Users.country, 
               Sales.transaction_id,Sales.product_id, Sales.quantity, Sales.billing_amount, Sales.timestamp
        FROM Users
        JOIN Sales ON Users.user_id = Sales.user_id
    '''
    df = pd.read_sql_query(query, conn)
    st.table(df)
    conn.close()

