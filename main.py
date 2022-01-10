#!/usr/bin/env python

#from Tkinter import * # Label, Entry, Button, BooleanVar, IntVar, Menu, Checkbutton, Radiobutton, spinbox
import tkinter as tk
#from ttk import Combobox, Progressbar, ScrolledText
import tkinter.ttk as ttk
#import tkFont as tkfont
from tkinter import font as tkfont
import sqlite3
import csv
import os
import time
import threading
from datetime import datetime
import binascii
try:
    import matplotlib.pyplot as plt 
except:
    print("matplotlib.pyplot is not installed in your computer")
       
        
printing_flag = False
try:
    import win32api
    import win32print

    from docxtpl import DocxTemplate
    printing_flag = True
except:
    print("Receipt can not be priknted, due to un-availability of needed libraries") 

from digits2words import convert_to_words as digits2words





if printing_flag:
    print("Importing template document")
    template = DocxTemplate('Receipt_Template.docx')
receipt_table = []






def plotDailySale(year=2020,month=6,day=22):
    conn = sqlite3.connect('sales.db')
    crs = conn.cursor()
    global spin_plot_day
    global spin_plot_month
    global spin_plot_year
    
    day = int(spin_plot_day.get())
    month = int(spin_plot_month.get())
    year = int(spin_plot_year.get())
    year_month_day = str(year)+"_"+format(month,'02d')+"_"+format(day,'02d')
    
    months_with_31_days = [1,3,5,7,8,10,12]
    months_with_30_days = [4,6,9,11]
    if month in months_with_31_days:
        total_days = 31
    elif month in months_with_30_days:
        total_days = 30
    elif month == 2:
        if year%4 == 0:
            total_days = 29
        else:
            total_days = 28
    else:
         print("wrong month entered")
    if day > total_days:
        print("Wrong Date")
        print("Total days in month "+str(month)+" are "+str(total_days))
        return 1
    total_hours = 24
    total_per_hour_expected_sales_count = 500
    total_sale_per_hour = [0 for i in range(total_hours)]
    date = [[0 for i in range(total_per_hour_expected_sales_count)] for j in range(total_hours)]
    
    for i in range(0,total_hours):
        this_iter_hour = format(i,'02d')
        output=crs.execute("SELECT SUB_TOTAL from SALES WHERE DATE LIKE \'"+year_month_day+"\' AND TIME LIKE \'"+this_iter_hour+"%\'")
        count=0
        for j in output:
            #print i-1,count
            date[i-1][count] = int(j[0])
            total_sale_per_hour[i-1] += date[i-1][count]
            count += 1
    #print date
    #print ""
    #print total_sale_per_date
    # x axis values 
    x = range(0,total_hours)
    # corresponding y axis values 
    y = total_sale_per_hour
      
    # plotting the points  
    #plt.plot(x, y)
    #plt.stem(x, y)
    tick_label = x
    
    plt.figure(2)
    plt.bar(x, y, tick_label = tick_label, width = 0.8)
    # setting x and y axis range 
    plt.ylim(0,max(100,max(total_sale_per_hour))) 
    plt.xlim(0,total_hours) 
    # naming the x axis 
    plt.xlabel("Hours (Day="+format(day,'02d')+")") 
    # naming the y axis 
    plt.ylabel('Sale (PKR)') 
      
    # giving a title to my graph 
    plt.title('Sales per Day') 
      
    # function to show the plot 
    plt.show() 
    
def plotMonthlySale(year=2020,month=6):
    conn = sqlite3.connect('sales.db')
    crs = conn.cursor()
    global spin_plot_month
    global spin_plot_year
    month = int(spin_plot_month.get())
    year = int(spin_plot_year.get())
    year_month = str(year)+"_"+format(month,'02d')
    
    first_day_of_month = datetime(year, month, 1).weekday() # where Monday is 0 and Sunday is 6
    days_of_week = [0,1,2,3,4,5,6]*6
    day_names_of_week = ['M','T','W','T','F','S','S']*6
    
    months_with_31_days = [1,3,5,7,8,10,12]
    months_with_30_days = [4,6,9,11]
    if month in months_with_31_days:
        total_days = 31
    elif month in months_with_30_days:
        total_days = 30
    elif month == 2:
        if year%4 == 0:
            total_days = 29
        else:
            total_days = 28
    else:
         print("wrong month entered")
         return 1
    #print "total_days",total_days
    days_of_month = days_of_week[first_day_of_month:total_days+first_day_of_month]
    day_names_of_month = day_names_of_week[first_day_of_month:total_days+first_day_of_month]
    #print "days_of_month",days_of_month
    #print "day_names_of_month",day_names_of_month
    
    total_per_day_expected_sales_count = 5000
    total_sale_per_date = [0 for i in range(total_days)]
    date = [[0 for i in range(total_per_day_expected_sales_count)] for j in range(total_days)]
    
    for i in range(1,total_days+1):
        this_iter_date = format(i,'02d')
        output=crs.execute("SELECT SUB_TOTAL from SALES WHERE DATE LIKE \'"+year_month+"_"+this_iter_date+"\'")
        count=0
        for j in output:
            #print i-1,count
            date[i-1][count] = int(j[0])
            total_sale_per_date[i-1] += date[i-1][count]
            count += 1
    #print date
    #print ""
    #print total_sale_per_date
    # x axis values 
    x = range(1,total_days+1)
    # corresponding y axis values 
    y = total_sale_per_date
      
    # plotting the points  
    #plt.plot(x, y)
    #plt.stem(x, y)
    tick_label = [str(w[0])+""+w[1] for w in zip(x,day_names_of_month)]
    print(tick_label)
    plt.figure(1)
    plt.bar(x, y,tick_label = tick_label, width = 0.8)
    plt.bar(x, y, width = 0.8)
    #plt.plot(x,days_of_month)
    # setting x and y axis range 
    plt.ylim(0,max(100,max(total_sale_per_date))) 
    plt.xlim(1,total_days) 
    # naming the x axis 
    plt.xlabel("Dates (month="+format(month,'02d')+")") 
    # naming the y axis 
    plt.ylabel('Sale (PKR)') 
      
    # giving a title to my graph 
    plt.title('Sales per Month') 
      
    # function to show the plot 
    plt.show() 









current_version = "3.0"

root_window = tk.Tk() 
root_window.title("Janjua Mart ePOS ver"+current_version) # introduced crc in rx
root_window.geometry('1260x1000')


add_item_window = 0
    
tab_sale_row = 0
tab_inventory_row = 0
tab_add_item_row = 0

max_name_length = 25
max_purchase_list = 50
max_len_search_list = 50
searched_data_from_barcode = [] #[[0 for x in xrange(max_len_search_list)] for x in xrange(max_len_search_list)]

gTotal_discount = 0

def create_table():
    conn = sqlite3.connect('database.db')
    crs = conn.cursor()
    print("Opened database successfully")
    try:
        crs.execute('''CREATE TABLE DATABASE
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                 NAME           TEXT    NOT NULL,
                 BARCODE           TEXT,
                 SALE_PRICE            INT     NOT NULL,
                 PURCHASE_PRICE            REAL);''')
        print("Table created successfully")
        conn.close()
    except:
        print("Databsae already exists")
def create_sales_table():
    conn = sqlite3.connect('sales.db')
    crs = conn.cursor()
    print("Opened database successfully")
    try:
        crs.execute('''CREATE TABLE SALES
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                 DATE           TEXT NOT NULL,
                 TIME           TEXT NOT NULL,
                 NAME           TEXT    NOT NULL,
                 SALE_PRICE            INT     NOT NULL,
                 PURCHASE_PRICE            REAL,
                 QTY            INT NOT NULL,
                 SUB_TOTAL            REAL);''')
        print("Table created successfully")
        conn.close()
    except:
        print("Databsae already exists")

def search_barcode_name(barcode_search='',name_search=''):
    #barcode_search = '123457'
    conn = sqlite3.connect('database.db')
    crs = conn.cursor()
    found_barcode = False
    found_name = False
    add_new_item_prompt = False
    global max_len_search_list
    searched_data = [] #[[0 for x in xrange(max_len_search_list)] for x in xrange(max_len_search_list)]
    try:
        int(barcode_search)
        is_integer=True
    except:
        is_integer=False
    if is_integer==True and len(barcode_search)>3:
        add_new_item_prompt = True
        cursor = crs.execute("SELECT id, name, barcode,sale_price, purchase_price from DATABASE WHERE barcode="+barcode_search)
        found_count = 0
        row_nmbr=0
        for row in cursor:
           found_barcode = True
           searched_data.append(list(row))
           '''
           searched_data[row_nmbr][0]=row[0]
           searched_data[row_nmbr][1]=row[1]
           #searched_data[row_nmbr][2]=row[2]
           searched_data[row_nmbr][2]=row[3]
           searched_data[row_nmbr][3]=row[4]
           '''
           row_nmbr=row_nmbr+1
           found_count = found_count + 1
           if (row_nmbr) == max_len_search_list:
               break
    if found_barcode == False and len(name_search)>2:
        print("Barcode Not Found")
        #name_search = '7up'
        cursor = crs.execute("SELECT id, name, barcode,sale_price, purchase_price from DATABASE WHERE NAME LIKE \'%"+name_search+"%\'")
        found_name = False
        found_count = 0
        row_nmbr=0
        for row in cursor:
           found_count = found_count + 1
           found_name = True
           #print row_nmbr
           searched_data.append(list(row))
           '''
           searched_data[row_nmbr][0]=row[0]
           searched_data[row_nmbr][1]=row[1]
           #searched_data[row_nmbr][2]=row[2]
           searched_data[row_nmbr][2]=row[3]
           searched_data[row_nmbr][3]=row[4]
           '''
           row_nmbr=row_nmbr+1
           found_count = found_count + 1
           if (row_nmbr) == max_len_search_list:
               break
        if found_name == False:
            print("Name Not Found")
        print("Operation done successfully")
    conn.close()
    if add_new_item_prompt == True and found_barcode == False:
        print("This product should be added in database")
        #print "Do you want to add a new product?"
        #add_item_window_show(barcode=barcode_search)
    return (found_barcode or found_name),searched_data

def import_database(n=0):
    global btn_import_database
    try:
        os.remove("database.db")
        
    except:
        print("database.db not found, creating it")
        
        btn_import_database.configure(bg='red')
    database_csv = [] # [[0 for x in xrange(1000)] for x in xrange(1000)]
    try:
        with open('database.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    #print row[0],row[1],row[2],row[3],row[4]
                    line_count += 1
                else:
                    database_csv.append([row[0],row[1],row[2],row[3],row[4]])
                    '''
                    database_csv[line_count-1][0] = row[0]
                    database_csv[line_count-1][1] = row[1]
                    database_csv[line_count-1][2] = row[2]
                    database_csv[line_count-1][3] = row[3]
                    database_csv[line_count-1][4] = row[4]
                    '''
                    print(row[0],row[1],row[2],row[3],row[4])
                    line_count += 1
            print("Processed lines.")
            btn_import_database.configure(bg='green')
    except:
        print("Some Error Occured, in reading ")
        btn_import_database.configure(bg='red')
    create_table()
    conn = sqlite3.connect('database.db')
    for n in range(0,line_count-1):
        crs = conn.cursor()
        
        crs.execute("INSERT INTO DATABASE (NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE) \
              VALUES (?,?,?,?)",(database_csv[n][1] , database_csv[n][2], database_csv[n][3], database_csv[n][4]));
        '''
        crs.execute("INSERT INTO DATABASE (NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE) \
              VALUES (?,?,?,?)",(database_csv[n][1] , database_csv[n][2], database_csv[n][3], database_csv[n][4]));
        '''
                    
        try:
            conn.commit()
            btn_import_database.configure(bg='green')
        except:
            print("Commit Error")
            btn_import_database.configure(bg='red')
    print("Records created successfully")
    conn.close()


def add_item_window_show(name='',barcode=''):
    global add_item_window
    global root_window
    global max_name_length
    row_nmbr = 0
    add_item_window = tk.Toplevel(root_window)
    tab_add_item = ttk.Frame(add_item_window, width=300, height=100)
    tab_add_item.pack()
    
    
    def destroy_add_item_window(n=0):
        add_item_window.destroy()
    
    lbl = tk.Label(tab_add_item, text="Barcode")
    lbl.grid(column=0, row=row_nmbr)
    lbl = tk.Label(tab_add_item, text="Name")
    lbl.grid(column=1, row=row_nmbr)
    lbl = tk.Label(tab_add_item, text="Price")
    lbl.grid(column=2, row=row_nmbr)
    lbl = tk.Label(tab_add_item, text="Purchase")
    lbl.grid(column=3, row=row_nmbr)
    row_nmbr=row_nmbr+1
    
    
    txt_prod_barcode_new = tk.Entry(tab_add_item,text=barcode,width=max_name_length)
    txt_prod_barcode_new.grid(column=0,row=row_nmbr)
    txt_prod_barcode_new.delete(0,20)
    txt_prod_barcode_new.insert(0,str(barcode))
    txt_prod_name_new = tk.Entry(tab_add_item,text=name,width=max_name_length)
    txt_prod_name_new.grid(column=1,row=row_nmbr)
    txt_prod_sale_price_new = tk.Entry(tab_add_item,width=7)
    txt_prod_sale_price_new.grid(column=2,row=row_nmbr)
    txt_prod_purchase_price_new = tk.Entry(tab_add_item,width=7)
    txt_prod_purchase_price_new.grid(column=3,row=row_nmbr)
    row_nmbr=row_nmbr+1
    def search_if_already_exists(n=0):
        bc_id = txt_prod_barcode_new.get()
        [found,searched_data] = search_barcode_name(barcode_search=bc_id,name_search="")
        print(found,searched_data)
        if found:
            print("Item already exists")
            txt_prod_barcode_new.delete(0,20)
            txt_prod_name_new.delete(0,30)
            txt_prod_sale_price_new.delete(0,30)
            txt_prod_purchase_price_new.delete(0,30)
            txt_prod_name_new.insert(0,searched_data[0][1])
            txt_prod_sale_price_new.insert(0,searched_data[0][3])
            txt_prod_purchase_price_new.insert(0,searched_data[0][4])
            btn_import_database.configure(bg='red')
            focus_on_item_barcode(0)
        else:
            print("Item does not exists")
            btn_import_database.configure(bg='green')
            txt_prod_name_new.delete(0,30)
            txt_prod_sale_price_new.delete(0,30)
            txt_prod_purchase_price_new.delete(0,30)
            focus_on_item_name(0)
            
    def add_to_database(ID=0,Name='',s_price=0,p_price=0,barcode=''):
        Name = txt_prod_name_new.get()
        
        s_price = float(str('0')+txt_prod_sale_price_new.get())
        p_price = float(str('0')+txt_prod_purchase_price_new.get())
        if p_price == "":
            p_price = s_price
        barcode = txt_prod_barcode_new.get()
        conn = sqlite3.connect('database.db')
        crs = conn.cursor()
        
        crs.execute("INSERT INTO DATABASE (NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE) \
                  VALUES (?,?,?,?)",(Name , barcode, s_price, p_price));
        try:
            conn.commit()
        except:
            print("Commit Error")
        print("Records created successfully")
        conn.close()
        destroy_add_item_window()
        add_item_window_show()
    def focus_on_item_barcode(self):
        txt_prod_barcode_new.focus_set()
    def focus_on_item_name(self):
        txt_prod_name_new.focus_set()
    def focus_on_item_s_price(self):
        txt_prod_sale_price_new.focus_set()
    def focus_on_item_p_price(self):
        txt_prod_purchase_price_new.focus_set()
    def focus_on_item_add_button(self):
        btn_import_database.focus_set()
    
    
    btn_import_database = tk.Button(tab_add_item, text="Add to Database", command=add_to_database)
    btn_import_database.grid(column=0,row=row_nmbr)
    btn_import_database.bind('<Return>',add_to_database)
    #txt_prod_barcode_new.bind('<Return>',focus_on_item_name)
    txt_prod_name_new.bind('<Return>',focus_on_item_s_price)
    txt_prod_sale_price_new.bind('<Return>',focus_on_item_p_price)
    txt_prod_purchase_price_new.bind('<Return>',focus_on_item_add_button)
    txt_prod_barcode_new.bind('<Return>',search_if_already_exists)
    txt_prod_barcode_new.focus_set()
    #add_item_window.mainloop()
    
    
def add_an_item_in_database(database_csv):
    
    conn = sqlite3.connect('database.db')
    crs = conn.cursor()
    
    crs.execute("INSERT INTO DATABASE (NAME,BARCODE,SALE_PRICE,PURCHASE_PRICE) \
              VALUES (?,?,?,?)",(database_csv[1] , database_csv[2], database_csv[3], database_csv[4]));
    try:
        conn.commit()
    except:
        print("Commit Error")
    print("Record created successfully")
    conn.close()



tab_control = ttk.Notebook(root_window)
tab_sale = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_sale, text='Sale')
def tab_sale_selected(event):
    print("Tab_sale Selected")
    global combo_barcode
    combo_barcode.focus_set()
tab_sale.bind('<Button-1>',tab_sale_selected) # selection of area of tab_sale
tab_sale.bind('<Leave>',tab_sale_selected) # selection of area of tab_sale
#tab_control.bind('<Button-1>',tab_sale_selected) # selection of any tab

def tab_inventory_selected(event):
    print("Tab_Inventory Selected")
tab_inventory = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_inventory, text='Inventory')
tab_control.grid(column=0)

tab_update_db = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_update_db, text='Update')
tab_control.grid(column=0)

tab_add_item = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_add_item, text='Add item')
tab_control.grid(column=0)

tab_analysis_db = ttk.Frame(tab_control, width=100, height=100)
tab_control.add(tab_analysis_db, text='Analysis')
tab_control.grid(column=0)

prod_nmbr_in_list = 0
def Barcode_Entry(event):
    global txt_prod_name
    global prod_nmbr_in_list
    global combo_barcode
    global searched_data_from_barcode
    global txt_total_paid
    global spin_prod_qty
    #print "Barcode Scanned",repr(event.char)
    barcode = combo_barcode.get()
    print(barcode)
    iesco_bill_detect = False
    len_barcode = len(barcode)
    combo_barcode.delete(0,50)
    combo_barcode.insert(0,"")
    if barcode == '' and prod_nmbr_in_list != 0 :
        txt_total_paid.focus_set()
        print("Sale Done")
        return 0
    elif barcode == '':
        print("Please write barcode or name in this field")
        return 0
    if len(barcode) > 40 and barcode[0] == 'E' and barcode[-1:] == 'E':
        #barcode = "E1514413295220006211607210000067290000072936E"
        iesco_bill_detect = False
        print("It might have info for IESCO Bill")
        iesco_ref = barcode[1:15]
        iesco_bill_due_date = barcode[19:19+6]
        due_date_year = 2000 + int(iesco_bill_due_date[4:6])
        due_date_month = int(iesco_bill_due_date[2:4])
        due_date_day = int(iesco_bill_due_date[0:2])
        iesco_bill_amount_in_due_date = int(barcode[25:25+9])
        print(iesco_ref,iesco_bill_amount_in_due_date,iesco_bill_due_date)
        
        date_now = datetime.now()
        due_date = datetime(day=due_date_day, month=due_date_month, year=due_date_year)
        timedelta = due_date - date_now
        remaining_days = (timedelta).days + 1
        if remaining_days>-1:
            add_new_prod(name="IESCO Bill ref#"+iesco_ref+" Due Date= "+iesco_bill_due_date,
                     price=iesco_bill_amount_in_due_date)
            if remaining_days == 0:
                timedelta_hrs = 24 - int(date_now.strftime('%I'))
                if int(timedelta_hrs) <7:   # 7hrs means from 5pm (24-7=17hrs)
                    add_new_prod(name="IESCO Bill Fee Last Hours",
                     price=10)
                else:
                    add_new_prod(name="IESCO Bill Fee",
                     price=10)
            else:
                add_new_prod(name="IESCO Bill Fee",
                 price=10)
            combo_barcode['values']= [""]
        else:
            print("ERROR:Due date has been passed"+str(remaining_days))
            combo_barcode['values']= [("ERROR:Due date has been passed"+str(remaining_days))]
        return 0
        
    if barcode[0] == '.':
        #print type(barcode)
        manual_price = barcode[1:len_barcode].split('.')[0]
        if ("." in barcode[1:len_barcode]):
            manual_name = barcode[1:len_barcode].split('.')[1]
            if manual_name == "":
                manual_name = "misc"
            add_new_prod(name=manual_name,price=manual_price)
        else:
            add_new_prod(name="misc",price=manual_price)
        return 0
    if barcode[0] == 'q':
        barcode = barcode[1:]
        
        if barcode.find(',')>-1:
            tgt_prod_new_qty = barcode.split(',')[0]
            if (barcode.split(',')[1])>0:
                tgt_prod_number = int(barcode.split(',')[1])
            else:
                tgt_prod_number = prod_nmbr_in_list
        else:
            tgt_prod_new_qty = float(barcode)
            tgt_prod_number = prod_nmbr_in_list
            
            
        print('quantity selection',tgt_prod_new_qty)
        spin_prod_qty[tgt_prod_number-1].delete(0,8)
        spin_prod_qty[tgt_prod_number-1].insert(0,tgt_prod_new_qty)
        update_prodtotal_total()
        return 0
        
        
    [found,searched_data] = search_barcode_name(barcode_search=barcode,name_search=barcode)
    searched_data_from_barcode = searched_data
    if found == True:
        combo_barcode['values'] = [("")]
        counter = 0
        for row in searched_data:
            NAME = row[1]
            print("Name",NAME)
            if counter == 0:
                combo_barcode['values']= [(NAME)]
            else:
                combo_barcode['values']= combo_barcode['values'] + (NAME,)
            counter += 1
            
        
        combo_barcode.current(0) #set the selected item
        #print "Present Index",combo_barcode.current()
        if counter == 1:    # if only one item was found in the database, then add to the sale list
            combo_barcode_selected()
    else:
        print("Not Found")
    
    combo_barcode.focus_set()

def update_total():#prod_nmbr_in_list1):
    global prod_nmbr_in_list
    global txt_prod_total
    global txt_total
    global gTotal_discount
    global spin_prod_disc
    global spin_prod_qty
    total = 0
    gTotal_discount = 0
    prod_nmbr_in_list1=prod_nmbr_in_list
    for n in range(0,prod_nmbr_in_list1):
        total = total + float(txt_prod_total[n].get())
        gTotal_discount = gTotal_discount + (float(spin_prod_disc[n].get())*float(spin_prod_qty[n].get()))
        #print "update_total.n",n
    txt_total.delete(0,20)
    txt_total.insert(0,str(total))
def update_prod_total(prod_nmbr_in_list1=1):
    global prod_nmbr_in_list
    global spin_prod_price
    global spin_prod_disc
    global spin_prod_qty
    global txt_prod_total
    prod_nmbr_in_list1=prod_nmbr_in_list
    try:
        for n in range(0,prod_nmbr_in_list1):
            #print "update_prod_total.prod_nmbr_in_list",n
            #print spin_prod_price[n].get()
            price = float(spin_prod_price[n].get())
            disc = float(spin_prod_disc[n].get())
            quantity = float(spin_prod_qty[n].get())
            subtotal = (price-disc)*quantity
            txt_prod_total[n].delete(0,20)
            txt_prod_total[n].insert(0,subtotal)
        return subtotal
    except:
        print("Invalid values in sale area")
        return 0
    #update_total()
def update_prodtotal_total(n=0):
    global prod_nmbr_in_list
    update_prod_total()
    update_total()
def add_new_prod(name='',price=0,disc=0,qty=0,prod_total=0):
    global tab_sale_row
    global txt_prod_name
    global spin_prod_price
    global spin_prod_qty
    global spin_prod_disc
    global txt_prod_total
    global lbl_sr_nmbr_var
    global txt_prod_name_var
    global spin_prod_price_var
    global spin_prod_qty_var
    global spin_prod_disc_var
    global txt_prod_total_var    
    global prod_nmbr_in_list
    global max_name_length
    global lbl_sr_nmbr_value
    global txt_total_var
    
    
    
    try:
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
    except:
        print("Invalid value in sale area")
    
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
    
    spin_prod_disc_var[prod_nmbr_in_list]=tk.StringVar()
    spin_prod_disc[prod_nmbr_in_list] = tk.Spinbox(tab_sale, textvariable=spin_prod_disc_var[prod_nmbr_in_list], from_=0, to=20000,command=update_prodtotal_total, width=5)
    spin_prod_disc[prod_nmbr_in_list].grid(column=4,row=tab_sale_row)
    spin_prod_disc[prod_nmbr_in_list].delete(0,8)
    spin_prod_disc[prod_nmbr_in_list].insert(0,disc)
    spin_prod_disc[prod_nmbr_in_list].bind('<KeyRelease>',update_prodtotal_total)
    
    txt_prod_total_var[prod_nmbr_in_list]=tk.StringVar()
    txt_prod_total[prod_nmbr_in_list] = tk.Entry(tab_sale, textvariable=txt_prod_total_var[prod_nmbr_in_list],width=8)
    txt_prod_total[prod_nmbr_in_list].grid(column=5,row=tab_sale_row)
    
    prod_nmbr_in_list = prod_nmbr_in_list + 1
    sub_total = update_prod_total()
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
    print("Ran")


def cancel_and_new_sale(x=0):
    global lbl_sr_nmbr_value
    global txt_prod_name
    global spin_prod_price
    global spin_prod_disc
    global spin_prod_qty
    global txt_prod_total
    global prod_nmbr_in_list
    global lbl_sr_nmbr_value_var
    global combo_barcode
    global txt_total
    global txt_total_paid
    global lbl_change_back_var
    
    for n in range(0,prod_nmbr_in_list):
        
        lbl_sr_nmbr_value[n].destroy()
        txt_prod_name[n].destroy()
        spin_prod_price[n].destroy()
        spin_prod_disc[n].destroy()
        spin_prod_qty[n].destroy()
        txt_prod_total[n].destroy()
    
    #calc_change_wind_show(float(txt_total.get()))
    combo_barcode.focus_set()
    txt_total.delete(0,20)
    txt_total.insert(0,0)
    txt_total_paid.delete(0,20)
    txt_total_paid.insert(0,"")
    lbl_change_back_var.set(0)
    prod_nmbr_in_list=0
def save_and_new_sale(x=0):
    global lbl_sr_nmbr_value
    global txt_prod_name
    global spin_prod_price
    global spin_prod_disc
    global spin_prod_qty
    global txt_prod_total
    global prod_nmbr_in_list
    global lbl_sr_nmbr_value_var
    global combo_barcode
    global txt_total
    global txt_total_paid
    global lbl_change_back_var
    global receipt_table
    global gTotal_discount
    global template
    
    
    cash_paid_by_customer = float(txt_total_paid.get())
    change_back_to_customer = float(lbl_change_back_var.get())
    
    
    serial_num = 0
    with open('non_volatile_var.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0]=="SERIAL_NUM":
                    serial_num = int(row[1])
                    print("Serial_Number",serial_num)
                    break
    
    
    
    total_qty = 0
    create_sales_table()
    conn = sqlite3.connect('sales.db')
    crs = conn.cursor()
        
    time_now = datetime.now()
    
    day = time_now.strftime('%d')
    month = time_now.strftime('%b')
    year = time_now.strftime('%Y')
    hour = time_now.strftime('%I')
    minute = time_now.strftime('%M')
    sec = time_now.strftime('%S')
    filename = "Invoices/invoice_"+str(serial_num)+"_"+day+"_"+month+"_"+year+"_"+hour+"_"+minute+"_"+sec+".csv"
    f = open(filename,'w+')  # write in text mode
    #f = open("invoices/"+"qwer.csv",'w+')  # write in text mode
    dt_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
    d_string = time_now.strftime("%Y_%m_%d")
    t_string = time_now.strftime("%H_%M_%S")
    f.write(","+dt_string+ ",Janjua Mart,03450508263\n")
    f.write( "Sr.no.,Name,Price,Quantity,Subtotal\n")
    receipt_table = []
    for n in range(0,prod_nmbr_in_list):
        prod_srno = lbl_sr_nmbr_value[n].cget("text")
        prod_name = txt_prod_name[n].get()
        prod_price = spin_prod_price[n].get()
        prod_disc = spin_prod_disc[n].get()
        prod_qty = spin_prod_qty[n].get()
        prod_sub_total = txt_prod_total[n].get()
        prod_purchase_price = "0"
        f.write( ""+prod_srno+","+ prod_name +","+ prod_price+","+ prod_qty+","+prod_sub_total+"\n")
        crs.execute("INSERT INTO SALES (DATE,TIME,NAME,SALE_PRICE,PURCHASE_PRICE,QTY,SUB_TOTAL) \
              VALUES (?,?,?,?,?,?,?)",(d_string,t_string,prod_name,prod_price,prod_qty,prod_purchase_price,prod_sub_total));
        total_qty = total_qty + float(prod_qty)
        receipt_table.append({
            'srno': prod_srno,
            'name': prod_name,
            'qty': prod_qty,
            'price': prod_price,
            'disc': prod_disc,
            'subtotal': prod_sub_total,
            })
        
        lbl_sr_nmbr_value[n].destroy()
        txt_prod_name[n].destroy()
        spin_prod_price[n].destroy()
        spin_prod_qty[n].destroy()
        spin_prod_disc[n].destroy()
        txt_prod_total[n].destroy()
    try:
        conn.commit()
    except:
        print("Commit Error")
    print("Records created successfully")
    conn.close()
    grand_total = txt_total.get()
    gtotal_words = digits2words(grand_total) + " Only"
    print(gtotal_words)
    serial_num_str = format(serial_num,'05d')
    #Declare template variables
    context = {
        'cashier_name': 'Asad Mehmood',
        'recno': serial_num_str,
        'date': day+"/"+month+"/"+year,
        'time': hour+':'+minute+':'+sec+' '+datetime.now().strftime('%p'),
        'gtotal_words': gtotal_words,
        'cash_by_customer': str(cash_paid_by_customer),
        'cash_to_customer': str(change_back_to_customer),
        'receipt_table': receipt_table,
        'gdisc': gTotal_discount,
        'total_qty': int(total_qty),
        'gtotal': grand_total
        }
    
    #try:
    if True:
        import_disc_template = False
        #print(len(receipt_table),receipt_table)
        #print("gTotal_discount",gTotal_discount)
        for i in range(0,len(receipt_table)):
            row = receipt_table[i]
            if int(row['disc'])>0:
                import_disc_template = True
                break
        if import_disc_template:
            template = DocxTemplate('Receipt_Template_disc.docx')
        else:
            template = DocxTemplate('Receipt_Template.docx')
        #Render automated report
        template.render(context)
        filename = "invoice_"+serial_num_str+"_"+day+"_"+month+"_"+year+"_"+hour+"_"+minute+"_"+sec+".docx"
        #filename = "generated_report.docx"
        template.save(filename)
        time.sleep(0.1)
        
        win32api.ShellExecute (
          0,
          "print",
          filename,
          #
          # If this is None, the default printer will
          # be used anyway.
          #
          '/d:"%s"' % win32print.GetDefaultPrinter (),
          ".",
          0
        )
        
    #except:
       # print("")
    

    f.write("\n,,,Total,"+grand_total)
    f.write("\n,,,,"+digits2words(grand_total))
    f.close()
    
    serial_num += 1
    
    f = open("non_volatile_var.csv",'w+')
    f.write("SERIAL_NUM,"+str(serial_num))
    f.close()
    


    #calc_change_wind_show(float(txt_total.get()))
    combo_barcode.focus_set()
    txt_total.delete(0,20)
    txt_total.insert(0,0)
    txt_total_paid.delete(0,20)
    txt_total_paid.insert(0,"")
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
lbl_time_date = tk.Label(tab_sale, font=tkfont.Font(size=15), textvariable=lbl_time_date_var,width=17)
lbl_time_date.grid(column=1, row=tab_sale_row)
lbl_time_date_var.set("0")
t1 = periodic_update_time_date()
t1.start()
lbl = tk.Label(tab_sale, font=tkfont.Font(size=15), text="Return")
lbl.grid(column=4, row=tab_sale_row)
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
combo_barcode.bind('<Return>',Barcode_Entry) # ahsann debug
def combo_barcode_selected(n=0):
    global combo_barcode
    global searched_data_from_barcode
    #print searched_data_from_barcode
    current_selected_index = combo_barcode.current()
    print("combo_barcode_selected")
    add_new_prod(name=searched_data_from_barcode[current_selected_index][1],
                 price=searched_data_from_barcode[current_selected_index][3])
    
    combo_barcode['values'] = [("")]
    combo_barcode.delete(0,50)
    combo_barcode.insert(0,"")
combo_barcode.bind('<<ComboboxSelected>>', combo_barcode_selected)

def combo_barcode_keypressed(event):
    #print str(event.char).encode('hex') == '03' # ctrl+c
    #print str(event.char).encode('hex') == '7f' # del  # event.keysym Delete
    #print str(event.char).encode('hex') == '1b' # esc  # event.keysym Escape
    print (type(event.keysym),event.keysym)
    print ('----------------------------------------------')
    if event.keysym == 'Escape' :
        cancel()
        return 0
    elif event.keysym == 'Delete':
        cancel_item()
        return 0
    
    global txt_prod_name
    global prod_nmbr_in_list
    global combo_barcode
    global searched_data_from_barcode
    global txt_total_paid
    #print "Barcode Scanned",repr(event.char)
    barcode = combo_barcode.get()
    #print barcode
        
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
        
        #combo_barcode.current(0) #set the selected item
        #print "Present Index",combo_barcode.current()
        #if counter == 1:
            #combo_barcode_selected()
    else:
        print("Not Found")
        combo_barcode['values'] = [("")]
    
    combo_barcode.focus_set()
    
    
combo_barcode.bind('<Key>', combo_barcode_keypressed)


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
txt_total_paid.bind('<Return>',save_and_new_sale)
    
#btn_save_and_new = tk.Button(tab_sale, text="Save&New", command=save_and_new_sale)
#btn_save_and_new.grid(column=3,row=tab_sale_row)
#btn_save_and_new.bind('<Return>',save_and_new_sale)

def cancel_item(item_number = 65535):
    global tab_sale_row
    global txt_prod_name
    global spin_prod_price
    global spin_prod_qty
    global spin_prod_disc
    global txt_prod_total
    global lbl_sr_nmbr_var
    global txt_prod_name_var
    global spin_prod_price_var
    global spin_prod_qty_var
    global spin_prod_disc_var
    global txt_prod_total_var    
    global prod_nmbr_in_list
    global max_name_length
    global lbl_sr_nmbr_value
    global txt_total_var
    
    prev_prod_nmbr_in_list = prod_nmbr_in_list
    prev_table = []
    #try:
    if True:
        for n in range(0,prev_prod_nmbr_in_list):
            print(n,item_number,prev_prod_nmbr_in_list)
            if n == item_number-1:  # index starts from 0
                print('condition true if n == item_number-1:  # index starts from 0')
                prod_nmbr_in_list = prod_nmbr_in_list - 1
                continue
            #if item_number == 65535:
            #    print('condition true if item_number == 655353 and n == prev_prod_nmbr_in_list - 1:')
            #    prod_nmbr_in_list = prod_nmbr_in_list - 1
            #    continue
            table = []
            table.append(txt_prod_name[n].get())
            table.append(spin_prod_price[n].get())
            table.append(spin_prod_qty[n].get())
            table.append(spin_prod_disc[n].get())
            table.append(txt_prod_total[n].get())
            prev_table.append(table)
    #except:
    #    print("Invalid value in sale area")
    if item_number == 65535:
        print (prev_table,prev_table[0:-1])
        prev_table = prev_table[0:-1]
        prod_nmbr_in_list = prod_nmbr_in_list - 1
    print (prev_table)
    cancel()
    prod_nmbr_in_list = 0 # it is forcely to zero in cancel()
    tab_sale_row = 4
    for prod_nmbr in range(0,prod_nmbr_in_list):
        print 
        lbl_sr_nmbr_value_var[prod_nmbr] = tk.StringVar()
        lbl_sr_nmbr_value[prod_nmbr] = tk.Label(tab_sale, textvariable=lbl_sr_nmbr_value_var[prod_nmbr])
        lbl_sr_nmbr_value[prod_nmbr].grid(column=0, row=tab_sale_row)
        lbl_sr_nmbr_value_var[prod_nmbr].set(str(prod_nmbr+1)+".")

        txt_prod_name_var[prod_nmbr]=tk.StringVar()
        txt_prod_name[prod_nmbr] = tk.Entry(tab_sale, textvariable=txt_prod_name_var[prod_nmbr],width=max_name_length)
        txt_prod_name[prod_nmbr].grid(column=1,row=tab_sale_row)
        txt_prod_name[prod_nmbr].delete(0,max_name_length)
        txt_prod_name[prod_nmbr].insert(0,prev_table[prod_nmbr][0])
        
        spin_prod_price_var[prod_nmbr]=tk.StringVar()
        spin_prod_price[prod_nmbr] = tk.Spinbox(tab_sale, textvariable=spin_prod_price_var[prod_nmbr], from_=1, to=20000,command=update_prodtotal_total, width=5)
        spin_prod_price[prod_nmbr].grid(column=2,row=tab_sale_row)
        spin_prod_price[prod_nmbr].delete(0,8)
        spin_prod_price[prod_nmbr].insert(0,prev_table[prod_nmbr][1])
        spin_prod_price[prod_nmbr].bind('<KeyRelease>',update_prodtotal_total)
        
        
        spin_prod_qty_var[prod_nmbr]=tk.StringVar()
        spin_prod_qty[prod_nmbr] = tk.Spinbox(tab_sale, textvariable=spin_prod_qty_var[prod_nmbr], from_=0, to=100,command=update_prodtotal_total, width=5)
        spin_prod_qty[prod_nmbr].grid(column=3,row=tab_sale_row)
        spin_prod_qty[prod_nmbr].delete(0,8)
        spin_prod_qty[prod_nmbr].insert(0,prev_table[prod_nmbr][2])
        spin_prod_qty[prod_nmbr].bind('<KeyRelease>',update_prodtotal_total)
        
        spin_prod_disc_var[prod_nmbr]=tk.StringVar()
        spin_prod_disc[prod_nmbr] = tk.Spinbox(tab_sale, textvariable=spin_prod_disc_var[prod_nmbr], from_=0, to=20000,command=update_prodtotal_total, width=5)
        spin_prod_disc[prod_nmbr].grid(column=4,row=tab_sale_row)
        spin_prod_disc[prod_nmbr].delete(0,8)
        spin_prod_disc[prod_nmbr].insert(0,prev_table[prod_nmbr][3])
        spin_prod_disc[prod_nmbr].bind('<KeyRelease>',update_prodtotal_total)
        
        txt_prod_total_var[prod_nmbr]=tk.StringVar()
        txt_prod_total[prod_nmbr] = tk.Entry(tab_sale, textvariable=txt_prod_total_var[prod_nmbr],width=8)
        txt_prod_total[prod_nmbr].grid(column=5,row=tab_sale_row)
        txt_prod_total[prod_nmbr].delete(0,8)
        txt_prod_total[prod_nmbr].insert(0,prev_table[prod_nmbr][4])
        
        sub_total = update_prod_total()
        update_total()
        tab_sale_row = tab_sale_row + 1
        
        
    #sub_total = update_prod_total()
        
    #prod_nmbr_in_list = prod_nmbr_in_list + 1
    
    
def cancel(n=0):
    global combo_barcode
    global txt_total
    global prod_nmbr_in_list
    global lbl_change_back_var
    global txt_total_paid
    global lbl_sr_nmbr_value
    global txt_prod_name
    global spin_prod_price
    global spin_prod_qty
    global txt_prod_total
    for n in range(0,prod_nmbr_in_list):
        lbl_sr_nmbr_value[n].destroy()
        txt_prod_name[n].destroy()
        spin_prod_price[n].destroy()
        spin_prod_disc[n].destroy()
        spin_prod_qty[n].destroy()
        txt_prod_total[n].destroy()
    
    combo_barcode.focus_set()
    txt_total.delete(0,20)
    txt_total.insert(0,0)
    txt_total_paid.delete(0,20)
    txt_total_paid.insert(0,0)
    lbl_change_back_var.set(0)
    prod_nmbr_in_list=0
    combo_barcode['values'] = [("")]
    combo_barcode.delete(0,50)
    combo_barcode.insert(0,"")
btn_cancel = tk.Button(tab_sale, text="Cancel", command=cancel_and_new_sale)
btn_cancel.grid(column=3,row=tab_sale_row)
btn_cancel.bind('<Return>',cancel)


    
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
lbl = tk.Label(tab_sale, text="Discount")
lbl.grid(column=4, row=tab_sale_row)
lbl = tk.Label(tab_sale, text="Subtotal")
lbl.grid(column=5, row=tab_sale_row)
tab_sale_row=tab_sale_row+1

btn_add_item_database = tk.Button(tab_add_item, text="Add_Item", command=add_item_window_show)
btn_add_item_database.grid(column=0,row=tab_inventory_row)
btn_add_item_database.bind('<Return>',add_item_window_show)
#tab_inventory_row = tab_inventory_row + 1


btn_import_database = tk.Button(tab_inventory, text="Import", command=import_database)
btn_import_database.grid(column=0,row=tab_inventory_row)
btn_import_database.bind('<Return>',import_database)
tab_inventory_row = tab_inventory_row + 1


def export_database(n=0):
    #f = open("exp_database.csv",'w+')  # write in text mode
    f = open("database.csv",'w+')  # write in text mode
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




lbl_sr_nmbr_value_var = [0 for x in range(max_purchase_list)]
lbl_sr_nmbr_value = [0 for x in range(max_purchase_list)]

txt_prod_name_var = [0 for x in range(max_purchase_list)]
txt_prod_name = [0 for x in range(max_purchase_list)]

spin_prod_price_var= [0 for x in range(max_purchase_list)]
spin_prod_price = [0 for x in range(max_purchase_list)]

spin_prod_disc_var= [0 for x in range(max_purchase_list)]
spin_prod_disc = [0 for x in range(max_purchase_list)]

spin_prod_qty_var = [0 for x in range(max_purchase_list)]
spin_prod_qty = [0 for x in range(max_purchase_list)]

txt_prod_total_var = [0 for x in range(max_purchase_list)]
txt_prod_total = [0 for x in range(max_purchase_list)]

tab_sale_row = tab_sale_row + 1


def search_item_for_update(n=0):
    global combo_text_search_for_update
    global searched_data_from_barcode
    entered_text = combo_text_search_for_update.get()
    print(entered_text)
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
        print("Not Found")
    combo_text_search_for_update.focus_set()
    
combo_text_search_for_update = ttk.Combobox(tab_update_db, font=tkfont.Font(size=25), width=max_name_length)
combo_text_search_for_update.grid(column=1,row=0)
combo_text_search_for_update.bind('<Return>',search_item_for_update)
#combo_text_search_for_update.bind('<Key>',search_item_for_update) # ahsan debug
def update_item(n=0,name='',price='',purchase=''):
    global txt_prod_name_for_update
    global spin_prod_price_for_update_var
    global spin_prod_purch_price_for_update_var
    global max_name_length
    name = txt_prod_name_for_update.get()
    price = spin_prod_price_for_update.get()
    purchase = spin_prod_purch_price_for_update.get()
    print(name,price)
    conn = sqlite3.connect('database.db')
    crs = conn.cursor()
    exec_str = "UPDATE DATABASE SET SALE_PRICE = "+price+" WHERE NAME = \""+name+"\""
    crs.execute(exec_str)
    exec_str = "UPDATE DATABASE SET PURCHASE_PRICE = "+purchase+" WHERE NAME = \""+name+"\""
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
    print("combo_text_search_for_update_selected")
    
    name = searched_data_from_barcode[current_selected_index][1]
    price = searched_data_from_barcode[current_selected_index][3]
    purchased = searched_data_from_barcode[current_selected_index][4]
    txt_prod_name_for_update.delete(0,max_name_length)
    txt_prod_name_for_update.insert(0,name)
    spin_prod_price_for_update_var.set(price)
    spin_prod_purch_price_for_update_var.set(purchased)
    
    #update_item(name=name,price=price,purchase=purchased)
    combo_text_search_for_update['values'] = [("")]
    combo_text_search_for_update.delete(0,32)
    combo_text_search_for_update.insert(0,"")
combo_text_search_for_update.bind('<<ComboboxSelected>>', combo_text_search_for_update_selected)
#combo_text_search_for_update.bind('<<key>>', combo_text_search_for_update_selected)  # ahsan debug
#btn_update_item_1 = tk.Button(tab_update_db, text="Update Item", command=update_item)
#btn_update_item_1.grid(column=2,row=0)
#btn_update_item_1.bind('<Return>',update_item)


lbl = tk.Label(tab_update_db, text="Price")
lbl.grid(column=1, row=1)
lbl = tk.Label(tab_update_db, text="Purchase")
lbl.grid(column=2, row=1)
lbl = tk.Label(tab_update_db, text="Name")
lbl.grid(column=3, row=1)


spin_prod_price_for_update_var=tk.StringVar()
spin_prod_price_for_update= tk.Spinbox(tab_update_db, textvariable=spin_prod_price_for_update_var, from_=1, to=20000, width=5)
spin_prod_price_for_update.grid(column=1,row=2)
spin_prod_price_for_update.delete(0,8)
spin_prod_price_for_update.insert(0,"0")
spin_prod_price_for_update.bind('<Return>',update_item)

spin_prod_purch_price_for_update_var=tk.StringVar()
spin_prod_purch_price_for_update= tk.Spinbox(tab_update_db, textvariable=spin_prod_purch_price_for_update_var, from_=1, to=20000, width=5)
spin_prod_purch_price_for_update.grid(column=2,row=2)
spin_prod_purch_price_for_update.delete(0,8)
spin_prod_purch_price_for_update.insert(0,"0")
spin_prod_purch_price_for_update.bind('<Return>',update_item)

txt_prod_name_for_update= tk.Entry(tab_update_db,width=max_name_length)
txt_prod_name_for_update.grid(column=3,row=2)
txt_prod_name_for_update.delete(0,max_name_length)
txt_prod_name_for_update.insert(0,"NILL")
txt_prod_name_for_update.bind('<Return>',update_item)


    
btn_update_item = tk.Button(tab_update_db, text="Update Item", command=update_item)
btn_update_item.grid(column=4,row=2)
btn_update_item.bind('<Return>',update_item)



lbl = tk.Label(tab_analysis_db, text="Year")
lbl.grid(column=1, row=0)
lbl = tk.Label(tab_analysis_db, text="Month")
lbl.grid(column=2, row=0)
lbl = tk.Label(tab_analysis_db, text="Day")
lbl.grid(column=3, row=0)

btn_plot_monthly_sales = tk.Button(tab_analysis_db, text="Plot Monthly Sales", command=plotMonthlySale)
btn_plot_monthly_sales.grid(column=0,row=1)
btn_plot_monthly_sales.bind('<Return>',plotMonthlySale)


spin_plot_year_var=tk.StringVar()
spin_plot_year= tk.Spinbox(tab_analysis_db, textvariable=spin_plot_year_var, from_=2020, to=2030, width=5)
spin_plot_year.grid(column=1,row=1)

spin_plot_month_var=tk.StringVar()
spin_plot_month= tk.Spinbox(tab_analysis_db, textvariable=spin_plot_month_var, from_=1, to=12, width=5)
spin_plot_month.grid(column=2,row=1)

spin_plot_day_var=tk.StringVar()
spin_plot_day= tk.Spinbox(tab_analysis_db, textvariable=spin_plot_day_var, from_=1, to=31, width=5)
spin_plot_day.grid(column=3,row=1)

def set_today_date(n=0):
    global spin_plot_year
    global spin_plot_month
    global spin_plot_day
    year = str(datetime.now())[0:4]
    month = str(datetime.now())[5:7]
    day = str(datetime.now())[8:10]
    spin_plot_year.delete(0,8)
    spin_plot_year.insert(0,year)
    spin_plot_month.delete(0,8)
    spin_plot_month.insert(0,month)
    spin_plot_day.delete(0,8)
    spin_plot_day.insert(0,day)
    
    

btn_plot_daily_sales = tk.Button(tab_analysis_db, text="Today", command=set_today_date)
btn_plot_daily_sales.grid(column=4,row=1)
btn_plot_daily_sales.bind('<Return>',plotDailySale)
set_today_date()

btn_plot_daily_sales = tk.Button(tab_analysis_db, text="Plot Daily Sales", command=plotDailySale)
btn_plot_daily_sales.grid(column=0,row=2)
btn_plot_daily_sales.bind('<Return>',plotDailySale)


create_table()
create_sales_table()
#import_database()


combo_barcode.focus_set()
root_window.mainloop()
