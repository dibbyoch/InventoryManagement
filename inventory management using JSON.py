#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#modified code with excess products purchsed to avaid negative inventory count
#opening the records json file

import json
import time
import random
from ETL_process import update_database

def process_purchase(userinput_productid, userinput_quantity, Userinput_name, Userinput_number, Userinput_country, proceed_with_max_quantity=False):
    fd = open("Records.json",'r')
    js = fd.read()
    fd.close()
    records = json.loads(js)

    sd = open('sales.json','r')
    ss = sd.read()
    sd.close()
    sales_record = json.loads(ss) if ss else {}

    # Check if product exists
    if userinput_productid not in records:
        return None, None, None

    
    # Check if sufficient quantity is available
    product_quantity = int(records[userinput_productid]['Quantity'])
    if product_quantity < userinput_quantity:
        if proceed_with_max_quantity and product_quantity > 0:
            userinput_quantity = product_quantity
        else:
            return False, product_quantity, None
    
     # Update inventory quantity
    records[userinput_productid]['Quantity'] = str(product_quantity - userinput_quantity)

    # Calculate billing amount
    billing_amount = int(records[userinput_productid]['Price']) * userinput_quantity
    #creating the structure of sales record
        
    transaction_id = str(random.randint(10000, 99999))
    sales_entry = {
    "Name": Userinput_name,
    "Mobile": Userinput_number,
    "Country": Userinput_country,
    "Product_ID": userinput_productid,
    "Quantity": userinput_quantity,
    "Billing_Amount": str(int(records[userinput_productid]['Price']) * userinput_quantity),
    "Timestamp": time.ctime()
    }
    
    #updaing dictionary with trans_id record
    sales_record[transaction_id] = sales_entry
    
    
    #opening the file for updating the json records inrecords.json
    js = json.dumps(records)
    fd = open('C:/Users/PlethoraX/Desktop/Records.json','w')
    fd.write(js)
    fd.close()
    
    #sales file updation
    ss = json.dumps(sales_record, indent=4)
    sd = open('C:/Users/PlethoraX/Desktop/sales.json', 'w')
    sd.write(ss)
    sd.close()
    
    update_database()
    return True, transaction_id, billing_amount


# In[ ]:




