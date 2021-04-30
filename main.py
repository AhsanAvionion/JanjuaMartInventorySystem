#!/usr/bin/env python

#from Tkinter import * # Label, Entry, Button, BooleanVar, IntVar, Menu, Checkbutton, Radiobutton, spinbox
import Tkinter as tk
#from ttk import Combobox, Progressbar, ScrolledText
import ttk
import tkFont as tkfont
import sqlite3
import csv
import os
import time
import threading
from datetime import datetime

current_version = "1.0"

root_window = tk.Tk() 
root_window.title("Janjua Mart Inventory Management ver") # introduced crc in rx
root_window.geometry('1000x700')


add_item_window = 0
    
tab_sale_row = 0
tab_inventory_row = 0

max_name_length = 25
max_purchase_list = 50
max_len_search_list = 50
searched_data_from_barcode = [[0 for x in xrange(max_len_search_list)] for x in xrange(max_len_search_list)]


def create_table():
    conn = sqlite3.connect('database.db')
    print "Opened database successfully";
    try:
        conn.execute('''CREATE TABLE DATABASE
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                 NAME           TEXT    NOT NULL,
                 BARCODE           TEXT,
                 SALE_PRICE            INT     NOT NULL,
                 PURCHASE_PRICE            REAL);''')
        print "Table created successfully";
        conn.close()
    except:
        print "Databsae already exists"

def search_barcode_name(barcode_search='',name_search=''):
    #barcode_search = '123457'
    conn = sqlite3.connect('database.db')
    found_barcode = False
    found_name = False
    add_new_item_prompt = False
    global max_len_search_list
    searched_data = [[0 for x in xrange(max_len_search_list)] for x in xrange(max_len_search_list)]
    try:
        int(barcode_search)
        is_integer=True
    except:
        is_integer=False
    if is_integer==True and len(barcode_search)>3:
        add_new_item_prompt = True
        cursor = conn.execute("SELECT id, name, barcode,sale_price, purchase_price from DATABASE WHERE barcode="+barcode_search)
        found_count = 0
        row_nmbr=0
        for row in cursor:
           found_barcode = True
           searched_data[row_nmbr][0]=row[0]
           searched_data[row_nmbr][1]=row[1]
           #searched_data[row_nmbr][2]=row[2]
           searched_data[row_nmbr][2]=row[3]
           searched_data[row_nmbr][3]=row[4]
           row_nmbr=row_nmbr+1
           found_count = found_count + 1
           if (row_nmbr) == max_len_search_list:
               break
    if found_barcode == False and len(name_search)>2:
        print "Barcode Not Found"
        #name_search = '7up'
        cursor = conn.execute("SELECT id, name, barcode,sale_price, purchase_price from DATABASE WHERE NAME LIKE \'%"+name_search+"%\'")
        found_name = False
        found_count = 0
        row_nmbr=0
        for row in cursor:
           found_count = found_count + 1
           found_name = True
           #print row_nmbr
           searched_data[row_nmbr][0]=row[0]
           searched_data[row_nmbr][1]=row[1]
           #searched_data[row_nmbr][2]=row[2]
           searched_data[row_nmbr][2]=row[3]
           searched_data[row_nmbr][3]=row[4]
           row_nmbr=row_nmbr+1
           found_count = found_count + 1
           if (row_nmbr) == max_len_search_list:
               break
        if found_name == False:
            print "Name Not Found"
        print "Operation done successfully";
    conn.close()
    if add_new_item_prompt == True and found_barcode == False:
        print "Do you want to add a new product?"
        add_item_window_show(barcode=barcode_search)
    return (found_barcode or found_name),searched_data

def import_database(n=0):
    try:
        os.remove("database.db")
    except:
        print "database.db not found, creating it"
    database_csv = [[0 for x in xrange(10000)] for x in xrange(10000)]
    with open('database.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print row[0],row[1],row[2],row[3],row[4]
                line_count += 1
            else:
                database_csv[line_count-1][0] = row[0]
                database_csv[line_count-1][1] = row[1]
                database_csv[line_count-1][2] = row[2]
                database_csv[line_count-1][3] = row[3]
                database_csv[line_count-1][4] = row[4]
                
                #print row[0],row[1],row[2],row[3],row[4]
                line_count += 1
        print "Processed lines."
    
    create_table()
    conn = sqlite3.connect('database.db')
    for n in range(0,line_count-1):
        crs = conn.cursor()
        
        crs.execute("INSERT INTO DATABASE (NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE) \
              VALUES (?,?,?,?)",(database_csv[n][1] , database_csv[n][2], database_csv[n][3], database_csv[n][4]));
                    
        try:
            conn.commit()
        except:
            print "Commit Error"
    print "Records created successfully";
    conn.close()


def add_item_window_show(name='',barcode=''):
    global add_item_window
    global root_window
    global max_name_length
    row_nmbr = 0
    add_item_window = tk.Toplevel(root_window)
    tab_add_item = ttk.Frame(add_item_window, width=300, height=100)
    tab_add_item.pack()
    
    
    lbl = tk.Label(tab_add_item, text="Do you Want to add it in database")
    lbl.grid(column=0, row=row_nmbr)
    
    def destroy_add_item_window(n=0):
        add_item_window.destroy()
    btn_add_item_window_cancel = tk.Button(tab_add_item, text="No/Cancel", command=destroy_add_item_window)
    btn_add_item_window_cancel.grid(column=1,row=row_nmbr)
    btn_add_item_window_cancel.bind('<Return>',destroy_add_item_window)
    row_nmbr=row_nmbr+1
    
    lbl = tk.Label(tab_add_item, text="Name")
    lbl.grid(column=0, row=row_nmbr)
    lbl = tk.Label(tab_add_item, text="Price")
    lbl.grid(column=1, row=row_nmbr)
    lbl = tk.Label(tab_add_item, text="Buy")
    lbl.grid(column=2, row=row_nmbr)
    lbl = tk.Label(tab_add_item, text="Barcode")
    lbl.grid(column=3, row=row_nmbr)
    row_nmbr=row_nmbr+1
    
    txt_prod_name_new = tk.Entry(tab_add_item,text=name,width=max_name_length)
    txt_prod_name_new.grid(column=0,row=row_nmbr)
    txt_prod_sale_price_new = tk.Entry(tab_add_item,width=7)
    txt_prod_sale_price_new.grid(column=1,row=row_nmbr)
    txt_prod_purchase_price_new = tk.Entry(tab_add_item,width=7)
    txt_prod_purchase_price_new.grid(column=2,row=row_nmbr)
    txt_prod_barcode_new = tk.Entry(tab_add_item,text=barcode,width=max_name_length)
    txt_prod_barcode_new.grid(column=3,row=row_nmbr)
    txt_prod_barcode_new.delete(0,20)
    txt_prod_barcode_new.insert(0,str(barcode))
    row_nmbr=row_nmbr+1
    def add_to_database(ID=0,Name='',s_price=0,p_proce=0,barcode=''):
        Name = txt_prod_name_new.get()
        s_price = float(str('0')+txt_prod_sale_price_new.get())
        p_proce = float(str('0')+txt_prod_purchase_price_new.get())
        barcode = txt_prod_barcode_new.get()
        conn = sqlite3.connect('database.db')
        crs = conn.cursor()
        
        crs.execute("INSERT INTO DATABASE (NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE) \
                  VALUES (?,?,?,?)",(Name , barcode, s_price, p_proce));
        try:
            conn.commit()
        except:
            print "Commit Error"
        print "Records created successfully";
        conn.close()
        destroy_add_item_window()
    
    
    btn_import_database = tk.Button(tab_add_item, text="To Database", command=add_to_database)
    btn_import_database.grid(column=0,row=row_nmbr)
    btn_import_database.bind('<Return>',add_to_database)
    btn_add_item_window_cancel.focus_set()
    #add_item_window.mainloop()
    
    
def add_an_item_in_database(database_csv):
    
    conn = sqlite3.connect('database.db')
    crs = conn.cursor()
    
    crs.execute("INSERT INTO DATABASE (NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE) \
              VALUES (?,?,?,?)",(database_csv[1] , database_csv[2], database_csv[3], database_csv[4]));
    try:
        conn.commit()
    except:
        print "Commit Error"
    print "Record created successfully";
    conn.close()



tab_control = ttk.Notebook(root_window)
tab_sale = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_sale, text='Sale')
def tab_sale_selected(event):
    print "Tab_sale Selected"
    global combo_barcode
    combo_barcode.focus_set()
tab_sale.bind('<Button-1>',tab_sale_selected) # selection of area of tab_sale
tab_sale.bind('<Leave>',tab_sale_selected) # selection of area of tab_sale
#tab_control.bind('<Button-1>',tab_sale_selected) # selection of any tab

def tab_inventory_selected(event):
    print "Tab_Inventory Selected"
tab_inventory = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_inventory, text='Inventory')
tab_control.grid(column=0)

tab_update_db = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_update_db, text='Update')
tab_control.grid(column=0)


prod_nmbr_in_list = 0
def Barcode_Entry(event):
    global txt_prod_name
    global prod_nmbr_in_list
    global combo_barcode
    global searched_data_from_barcode
    #print "Barcode Scanned",repr(event.char)
    barcode = combo_barcode.get()
    print barcode
    combo_barcode.delete(0,32)
    combo_barcode.insert(0,"")
    if barcode == '':
        print "Please write barcode or name in this field"
        return 0
    if barcode[0] == '.':
        print type(barcode)
        if ("," in barcode):
            add_new_prod(name=barcode.split(',')[1],price=barcode[1:len(barcode)].split(',')[0])
        else:
            add_new_prod(name="misc",price=barcode[1:len(barcode)].split(',')[0])
        return 0
        
        
    [found,searched_data] = search_barcode_name(barcode_search=barcode,name_search=barcode)
    searched_data_from_barcode = searched_data
    if found == True:
        combo_barcode['values'] = [("")]
        counter = 0
        for n in range(0,len(searched_data)):
            NAME=searched_data[n][1]
            if NAME != 0:
                #print "Name",NAME
                if counter == 0:
                    combo_barcode['values']= [(NAME)]
                    #combo_barcode['values']= (NAME)
                else:
                    combo_barcode['values']= combo_barcode['values'] + (NAME,)
                #print combo_barcode['values']
                counter = counter + 1
        
        combo_barcode.current(0) #set the selected item
        #print "Present Index",combo_barcode.current()
        if counter == 1:
            combo_barcode_selected()
    else:
        print "Not Found"
    
    combo_barcode.focus_set()

def update_total():#prod_nmbr_in_list1):
    global prod_nmbr_in_list
    global txt_prod_total
    global txt_total
    total = 0
    prod_nmbr_in_list1=prod_nmbr_in_list
    for n in range(0,prod_nmbr_in_list1):
        total = total + float(txt_prod_total[n].get())
        #print "update_total.n",n
    txt_total.delete(0,20)
    txt_total.insert(0,str(total))
def update_prod_total(prod_nmbr_in_list1=1):
    global prod_nmbr_in_list
    global spin_prod_price
    global spin_prod_qty
    global txt_prod_total
    prod_nmbr_in_list1=prod_nmbr_in_list
    for n in range(0,prod_nmbr_in_list1):
        #print "update_prod_total.prod_nmbr_in_list",n
        #print spin_prod_price[n].get()
        price = float(spin_prod_price[n].get())
        quantity = float(spin_prod_qty[n].get())
        subtotal = price*quantity
        txt_prod_total[n].delete(0,20)
        txt_prod_total[n].insert(0,subtotal)
    #update_total()
def update_prodtotal_total(n=0):
    global prod_nmbr_in_list
    update_prod_total()
    update_total()
def add_new_prod(name='',price='',qty='',prod_total=''):
    global tab_sale_row
    global txt_prod_name
    global spin_prod_price
    global spin_prod_qty
    global txt_prod_total
    global lbl_sr_nmbr_var
    global txt_prod_name_var
    global spin_prod_price_var
    global spin_prod_qty_var
    global txt_prod_total_var    
    global prod_nmbr_in_list
    global max_name_length
    global lbl_sr_nmbr_value
    global txt_total_var
    
    
    for n in range(0,prod_nmbr_in_list):
        #print txt_prod_name[n].get(),name == txt_prod_name[n].get()
        if name == txt_prod_name[n].get() and name != 'misc':
            prev = spin_prod_qty[n].get()
            spin_prod_qty[n].delete(0,8)
            spin_prod_qty[n].insert(0,int(prev) + 1)
            #print "****************************Found"
            update_prod_total()
            update_total()
            return 
    
    lbl_sr_nmbr_value_var[prod_nmbr_in_list] = tk.StringVar()
    lbl_sr_nmbr_value[prod_nmbr_in_list] = tk.Label(tab_sale, textvariable=lbl_sr_nmbr_value_var[prod_nmbr_in_list])
    lbl_sr_nmbr_value[prod_nmbr_in_list].grid(column=0, row=tab_sale_row)
    lbl_sr_nmbr_value_var[prod_nmbr_in_list].set(str(prod_nmbr_in_list+1)+".")

    txt_prod_name_var[prod_nmbr_in_list]=tk.StringVar()
    txt_prod_name[prod_nmbr_in_list] = tk.Entry(tab_sale, textvariable=txt_prod_name_var[prod_nmbr_in_list],width=max_name_length)
    txt_prod_name[prod_nmbr_in_list].grid(column=1,row=tab_sale_row)
    txt_prod_name[prod_nmbr_in_list].delete(0,max_name_length)
    txt_prod_name[prod_nmbr_in_list].insert(0,name)
    
    spin_prod_price_var[prod_nmbr_in_list]=tk.StringVar()
    spin_prod_price[prod_nmbr_in_list] = tk.Spinbox(tab_sale, textvariable=spin_prod_price_var[prod_nmbr_in_list], from_=1, to=20000,command=update_prodtotal_total, width=5)
    spin_prod_price[prod_nmbr_in_list].grid(column=2,row=tab_sale_row)
    spin_prod_price[prod_nmbr_in_list].delete(0,8)
    spin_prod_price[prod_nmbr_in_list].insert(0,price)
    spin_prod_price[prod_nmbr_in_list].bind('<KeyRelease>',update_prodtotal_total)
    #spin_prod_price[prod_nmbr_in_list].bind('<Leave>',update_prodtotal_total)
    
    spin_prod_qty_var[prod_nmbr_in_list]=tk.StringVar()
    spin_prod_qty[prod_nmbr_in_list] = tk.Spinbox(tab_sale, textvariable=spin_prod_qty_var[prod_nmbr_in_list], from_=0, to=100,command=update_prodtotal_total, width=5)
    spin_prod_qty[prod_nmbr_in_list].grid(column=3,row=tab_sale_row)
    spin_prod_qty[prod_nmbr_in_list].delete(0,8)
    spin_prod_qty[prod_nmbr_in_list].insert(0,1)
    spin_prod_qty[prod_nmbr_in_list].bind('<KeyRelease>',update_prodtotal_total)
    #spin_prod_qty[prod_nmbr_in_list].bind('<Leave>',update_prodtotal_total)
    
    txt_prod_total_var[prod_nmbr_in_list]=tk.StringVar()
    txt_prod_total[prod_nmbr_in_list] = tk.Entry(tab_sale, textvariable=txt_prod_total_var[prod_nmbr_in_list],width=8)
    txt_prod_total[prod_nmbr_in_list].grid(column=4,row=tab_sale_row)
    
    prod_nmbr_in_list = prod_nmbr_in_list + 1
    update_prod_total()
    update_total()
    tab_sale_row = tab_sale_row + 1
def calc_change_wind_show(total_amount):
    global add_item_window
    global root_window
    global max_name_length
    row_nmbr = 0
    add_item_window = tk.Toplevel(root_window)
    tab_add_item = ttk.Frame(add_item_window, width=300, height=100)
    tab_add_item.pack()
    
    


    lbl = tk.Label(tab_add_item, text="Cash paid?")
    lbl.grid(column=0, row=row_nmbr)
    def calc_change_back(n=0):
        cust_paid = txt_cust_paid.get()
        x=int("0"+cust_paid)-total_amount
        lbl_cust_change_back_var.set(x)
        
    txt_cust_paid_var=tk.StringVar()
    txt_cust_paid = tk.Entry(tab_add_item, font=tkfont.Font(size=20), textvariable=txt_cust_paid_var,width=8)
    txt_cust_paid.grid(column=1,row=row_nmbr)
    txt_cust_paid.bind('<KeyRelease>',calc_change_back)
    lbl_cust_change_back_var=tk.StringVar()
    lbl_cust_change_back = tk.Label(tab_add_item, font=tkfont.Font(size=30), textvariable=lbl_cust_change_back_var)
    lbl_cust_change_back.grid(column=3, row=row_nmbr)
    lbl_cust_change_back_var.set(-1*int(total_amount))
    def destroy_add_item_window(n=0):
        add_item_window.destroy()
    #btn_add_item_window_cancel = tk.Button(tab_add_item, text="Done", command=destroy_add_item_window)
    #btn_add_item_window_cancel.grid(column=2,row=row_nmbr)
    #btn_add_item_window_cancel.bind('<Return>',destroy_add_item_window)
    txt_cust_paid.bind('<Return>',destroy_add_item_window)
    row_nmbr=row_nmbr+1
    txt_cust_paid.focus_set()
    print "Ran"
    
def save_and_new_sale(x=0):
    global lbl_sr_nmbr_value
    global txt_prod_name
    global spin_prod_price
    global spin_prod_qty
    global txt_prod_total
    global prod_nmbr_in_list
    global lbl_sr_nmbr_value_var
    global combo_barcode
    global txt_total
    global txt_total_paid
    global lbl_change_back_var
    
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    filename = dt_string
    f = open("Invoices/"+str(filename)+".csv",'w+')  # write in text mode
    #f = open("invoices/"+"qwer.csv",'w+')  # write in text mode
    f.write(","+dt_string+ ",Janjua Mart,03450508263\n")
    f.write( "Sr.no.,Name,Price,Quantity,Subtotal\n")
    for n in range(0,prod_nmbr_in_list):
        f.write( ""+lbl_sr_nmbr_value[n].cget("text")+","+ txt_prod_name[n].get()+","+ spin_prod_price[n].get()+","+ spin_prod_qty[n].get()+","+txt_prod_total[n].get()+"\n")
        lbl_sr_nmbr_value[n].destroy()
        txt_prod_name[n].destroy()
        spin_prod_price[n].destroy()
        spin_prod_qty[n].destroy()
        txt_prod_total[n].destroy()
    f.write("\n,,,Total,"+txt_total.get())
    f.close()
    #calc_change_wind_show(float(txt_total.get()))
    combo_barcode.focus_set()
    txt_total.delete(0,20)
    txt_total.insert(0,0)
    txt_total_paid.delete(0,20)
    txt_total_paid.insert(0,0)
    lbl_change_back_var.set(0)
    prod_nmbr_in_list=0
    
    
class periodic_update_time_date(threading.Thread):
    def __init__(self,t_name="default_name"):
        threading.Thread.__init__(self)
        self.name = t_name
        
    #Thread run function (called by thread_name.start())
    def run(self):
        global lbl_time_date_var
        while True:
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            #print dt_string
            lbl_time_date_var.set(dt_string)
            time.sleep(1)
            
    
    


lbl = tk.Label(tab_sale, text="Time")
lbl.grid(column=0, row=tab_sale_row)
lbl_time_date_var=tk.StringVar()
lbl_time_date = tk.Label(tab_sale, font=tkfont.Font(size=1), text="", textvariable=lbl_time_date_var,width=17)
lbl_time_date.grid(column=1, row=tab_sale_row)
lbl_time_date_var.set("0")
t1 = periodic_update_time_date()
t1.start()
tab_sale_row=tab_sale_row+1

lbl = tk.Label(tab_sale, text="Barcode")
lbl.grid(column=0, row=tab_sale_row)
# =============================================================================
# txt_barcode_var=tk.StringVar()
# txt_barcode = tk.Entry(tab_sale, textvariable=txt_barcode_var,width=18)
# txt_barcode.grid(column=1,row=tab_sale_row)
# txt_barcode.bind('<Return>',Barcode_Entry)
# =============================================================================

combo_barcode = ttk.Combobox(tab_sale, font=tkfont.Font(size=15), width=max_name_length)
combo_barcode.grid(column=1,row=tab_sale_row)
combo_barcode.bind('<Return>',Barcode_Entry)
def combo_barcode_selected(n=0):
    global combo_barcode
    global searched_data_from_barcode
    #print searched_data_from_barcode
    current_selected_index = combo_barcode.current()
    print "combo_barcode_selected"
    add_new_prod(name=searched_data_from_barcode[current_selected_index][1],
                 price=searched_data_from_barcode[current_selected_index][2])
    
    combo_barcode['values'] = [("")]
    combo_barcode.delete(0,32)
    combo_barcode.insert(0,"")
combo_barcode.bind('<<ComboboxSelected>>', combo_barcode_selected)


def calc_change_back(n=0):
    global txt_total_paid
    global txt_total
    cust_paid = float("0"+txt_total_paid.get())
    total_amount = float("0"+txt_total.get())
    x=cust_paid-total_amount
    lbl_change_back_var.set(x)
txt_total_paid_var=tk.StringVar()
txt_total_paid = tk.Entry(tab_sale, font=tkfont.Font(size=10),textvariable=txt_total_paid_var,width=8)
txt_total_paid.grid(column=2,row=tab_sale_row)
txt_total_paid.bind('<KeyRelease>',calc_change_back)
    
btn_save_and_new = tk.Button(tab_sale, text="Save&New", command=save_and_new_sale)
btn_save_and_new.grid(column=3,row=tab_sale_row)
btn_save_and_new.bind('<Return>',save_and_new_sale)


    
lbl_change_back_var=tk.StringVar()
lbl_change_back = tk.Label(tab_sale, font=tkfont.Font(size=10), textvariable=lbl_change_back_var,width=17)
lbl_change_back.grid(column=4, row=tab_sale_row)
lbl_change_back_var.set("0")

tab_sale_row=tab_sale_row+1



lbl = tk.Label(tab_sale, font=tkfont.Font(size=20), text="Total:")
lbl.grid(column=3, row=tab_sale_row)
txt_total_var=tk.StringVar()
txt_total = tk.Entry(tab_sale, font=tkfont.Font(size=30),textvariable=txt_total_var,width=8)
txt_total.grid(column=4,row=tab_sale_row)
txt_total.insert(0,"0")

tab_sale_row=tab_sale_row+1

lbl = tk.Label(tab_sale, text="Sr.no.")
lbl.grid(column=0, row=tab_sale_row)
lbl = tk.Label(tab_sale, text="Name")
lbl.grid(column=1, row=tab_sale_row)
lbl = tk.Label(tab_sale, text="Price")
lbl.grid(column=2, row=tab_sale_row)
lbl = tk.Label(tab_sale, text="Qty")
lbl.grid(column=3, row=tab_sale_row)
lbl = tk.Label(tab_sale, text="Subtotal")
lbl.grid(column=4, row=tab_sale_row)
tab_sale_row=tab_sale_row+1


btn_import_database = tk.Button(tab_inventory, text="Import", command=import_database)
btn_import_database.grid(column=0,row=tab_inventory_row)
btn_import_database.bind('<Return>',import_database)
tab_inventory_row = tab_inventory_row + 1


def export_database(n=0):
    f = open("exp_database.csv",'w+')  # write in text mode
    f.write( "ID,NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE\n")
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM DATABASE")

    rows = cur.fetchall()

    for row in rows:
        print(row)
        f.write( ""+str(row[0])+","+ str(row[1])+","+ str(row[2])+","+ str(row[3])+","+ str(row[4])+"\n")
    f.close()
        
    
btn_export_database = tk.Button(tab_inventory, text="Export", command=export_database)
btn_export_database.grid(column=0,row=tab_inventory_row)
btn_export_database.bind('<Return>',export_database)
tab_inventory_row = tab_inventory_row + 1


lbl_sr_nmbr_value_var = [0 for x in xrange(max_purchase_list)]
lbl_sr_nmbr_value = [0 for x in xrange(max_purchase_list)]

txt_prod_name_var = [0 for x in xrange(max_purchase_list)]
txt_prod_name = [0 for x in xrange(max_purchase_list)]

spin_prod_price_var= [0 for x in xrange(max_purchase_list)]
spin_prod_price = [0 for x in xrange(max_purchase_list)]

spin_prod_qty_var = [0 for x in xrange(max_purchase_list)]
spin_prod_qty = [0 for x in xrange(max_purchase_list)]

txt_prod_total_var = [0 for x in xrange(max_purchase_list)]
txt_prod_total = [0 for x in xrange(max_purchase_list)]

tab_sale_row = tab_sale_row + 1


def search_item_for_update(n=0):
    global combo_text_search_for_update
    global searched_data_from_barcode
    entered_text = combo_text_search_for_update.get()
    print entered_text
    combo_text_search_for_update.delete(0,32)
    combo_text_search_for_update.insert(0,"")
    [found,searched_data] = search_barcode_name(barcode_search=entered_text,name_search=entered_text)
    searched_data_from_barcode = searched_data
    if found == True:
        combo_text_search_for_update['values'] = [("")]
        counter = 0
        for n in range(0,len(searched_data)):
            NAME=searched_data[n][1]
            if NAME != 0:
                if counter == 0:
                    combo_text_search_for_update['values']= [(NAME)]
                else:
                    combo_text_search_for_update['values']= combo_text_search_for_update['values'] + (NAME,)
                counter = counter + 1
        
        combo_text_search_for_update.current(0) #set the selected item
        if counter == 1:
            combo_text_search_for_update_selected()
    else:
        print "Not Found"
    combo_text_search_for_update.focus_set()
    
combo_text_search_for_update = ttk.Combobox(tab_update_db, font=tkfont.Font(size=15), width=max_name_length)
combo_text_search_for_update.grid(column=1,row=0)
combo_text_search_for_update.bind('<Return>',search_item_for_update)
def update_item(n=0,name='',price='',purchase=''):
    global txt_prod_name_for_update
    global spin_prod_price_for_update_var
    global spin_prod_purch_price_for_update_var
    global max_name_length
    name = txt_prod_name_for_update.get()
    price = spin_prod_price_for_update.get()
    #purchase = spin_prod_purch_price_for_update.get()
    print name,price
    conn = sqlite3.connect('database.db')
    crs = conn.cursor()
    exec_str = "UPDATE DATABASE SET SALE_PRICE = "+price+" WHERE NAME = \""+name+"\""
    crs.execute(exec_str)
    conn.commit()
    conn.close()
    combo_text_search_for_update.focus_set()
    txt_prod_name_for_update.delete(0,max_name_length)
    txt_prod_name_for_update.insert(0,"NILL")
    
    spin_prod_price_for_update_var.set(0)
    spin_prod_purch_price_for_update_var.set(0)
                    
def combo_text_search_for_update_selected(n=0):
    global combo_text_search_for_update
    global searched_data_from_barcode
    global txt_prod_name_for_update
    global spin_prod_price_for_update_var
    global spin_prod_purch_price_for_update_var
    #print searched_data_from_barcode
    current_selected_index = combo_text_search_for_update.current()
    print "combo_text_search_for_update_selected"
    
    name = searched_data_from_barcode[current_selected_index][1]
    price = searched_data_from_barcode[current_selected_index][2]
    purchased = searched_data_from_barcode[current_selected_index][3]
    txt_prod_name_for_update.delete(0,max_name_length)
    txt_prod_name_for_update.insert(0,name)
    spin_prod_price_for_update_var.set(price)
    spin_prod_purch_price_for_update_var.set(purchased)
    
    #update_item(name=name,price=price,purchase=purchased)
    combo_text_search_for_update['values'] = [("")]
    combo_text_search_for_update.delete(0,32)
    combo_text_search_for_update.insert(0,"")
combo_text_search_for_update.bind('<<ComboboxSelected>>', combo_text_search_for_update_selected)
btn_update_item_1 = tk.Button(tab_update_db, text="Update Item", command=update_item)
btn_update_item_1.grid(column=2,row=0)
btn_update_item_1.bind('<Return>',update_item)


lbl = tk.Label(tab_update_db, text="Name")
lbl.grid(column=1, row=1)
lbl = tk.Label(tab_update_db, text="Price")
lbl.grid(column=2, row=1)
lbl = tk.Label(tab_update_db, text="Purchase")
lbl.grid(column=3, row=1)

txt_prod_name_for_update= tk.Entry(tab_update_db,width=max_name_length)
txt_prod_name_for_update.grid(column=1,row=2)
txt_prod_name_for_update.delete(0,max_name_length)
txt_prod_name_for_update.insert(0,"NILL")

spin_prod_price_for_update_var=tk.StringVar()
spin_prod_price_for_update= tk.Spinbox(tab_update_db, textvariable=spin_prod_price_for_update_var, from_=1, to=20000, width=5)
spin_prod_price_for_update.grid(column=2,row=2)
spin_prod_price_for_update.delete(0,8)
spin_prod_price_for_update.insert(0,"0")

spin_prod_purch_price_for_update_var=tk.StringVar()
spin_prod_purch_price_for_update= tk.Spinbox(tab_update_db, textvariable=spin_prod_purch_price_for_update_var, from_=1, to=20000, width=5)
spin_prod_purch_price_for_update.grid(column=3,row=2)
spin_prod_purch_price_for_update.delete(0,8)
spin_prod_purch_price_for_update.insert(0,"0")



    
btn_update_item = tk.Button(tab_update_db, text="Update Item", command=update_item)
btn_update_item.grid(column=4,row=2)
btn_update_item.bind('<Return>',update_item)

create_table()
#import_database()


combo_barcode.focus_set()

root_window.mainloop()
