#tkinter all
from tkinter import *
#main window
import tkinter as tk
#database connector
import mysql.connector
#dialogue box
from tkinter import messagebox
import tkinter.messagebox as mb
#font
from tkinter import font
#calendar date 
import datetime
from tkcalendar import DateEntry
#Image
from PIL import ImageTk, Image
#TreeView
import tkinter.ttk as ttk
from tkinter.ttk import Treeview, Style

# Create the main window
window = tk.Tk()
window.title("Login")
window.geometry("676x380")
#login image
url = ImageTk.PhotoImage(Image.open(r"C:\Users\fraud\Desktop\Job_Application_Tracker\login.png"))
p1 = Label(window, image = url)
p1.pack(side='top')

#functions
def login():
    username = entry_username.get()
    password = entry_password.get()

    #Connect to MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="job_application_tracker"
    )
    cursor = db.cursor()

    #Execute SQL query to fetch user data
    lquery = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(lquery, (username, password))
    #fetch
    result = cursor.fetchone()
    #clear entrty box
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

##############################################################################################################################################################################                  
#------------------CONNECTING_TO_THE_DATABASE---------------------------------------------------------------------------------------------------------------------------------
##############################################################################################################################################################################
    if result:
        connector = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="job_application_tracker"
        )
        cursor = connector.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS applications (ID INT AUTO_INCREMENT PRIMARY KEY, Date DATE,company VARCHAR(255),position VARCHAR(255),status VARCHAR(255))')
        connector.commit()

###############################################################################################################################################################################
#-------------------------FUNCTIONS-------------------------------------------------------------------------------------------------------------------------------------------#
###############################################################################################################################################################################

        def list_all():
            #global connector, table
        
            table.delete(*table.get_children())
    
            cursor.execute('SELECT * FROM applications')
            data = cursor.fetchall()

            for values in data:
                table.insert('', END, values=values)

        def submit():
            if not date.get() or not com.get() or not pos.get() or not sta.get():
                mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the SUBMIT button!")
            else:
                cursor.execute(
                    'INSERT INTO applications (Date, company, position, status) VALUES (%s, %s, %s, %s)',
                    (date.get_date(), com.get(), pos.get(), sta.get())
                )
                connector.commit()

                clear()
                list_all()
                mb.showinfo('Details added', 'The details you just entered has been added to the database')

        def clear():
            today_date = datetime.datetime.now().date()

            com.set('')
            pos.set('')
            sta.set('Applied')
            date.set_date(today_date)
            table.selection_remove(*table.selection())

        def view():
            if not table.selection():
                mb.showerror('No record selected', 'Please select an record from the table to view its details')

            current_selected_details = table.item(table.focus())
            values = current_selected_details['values']

            expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))

            date.set_date(expenditure_date)
            com.set(values[2])
            pos.set(values[3])
            sta.set(values[4])

        def delete_all():
            surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the details from the database?', icon='warning')

            if surety:
                table.delete(*table.get_children())

                cursor.execute('DELETE FROM applications')
                connector.commit()

                clear()
                list_all()
                mb.showinfo('All Details deleted', 'All the details were successfully deleted')
            else:
                mb.showinfo('Ok then', 'The task was aborted and no details was deleted!')

        def delete():
            if not table.selection():
                mb.showerror('No record selected!', 'Please select a record to delete!')
                return

            current_selected_details = table.item(table.focus())
            values_selected = current_selected_details['values']

            surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')

            if surety:
                cursor.execute('DELETE FROM applications WHERE ID=%s', (values_selected[0],))
                connector.commit()

                list_all()
                mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

        def edit():
            def edit_existing_details():

                current_selected_details = table.item(table.focus())
                contents = current_selected_details['values']

                cursor.execute('UPDATE applications SET Date = %s, company = %s, position = %s, status = %s WHERE ID = %s',
                              (date.get_date(), com.get(), pos.get(), sta.get(), contents[0]))
                connector.commit()

                clear()
                list_all()

                mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
                edit_btn.destroy()
                return

                if not table.selection():
                    mb.showerror('No details selected!', 'You have not selected any details in the table for us to edit; please do that!')
                    return

            view()

            edit_btn = Button(data_entry_frame, text='Edit details', font=btn_font, width=30,bg='darkgray', command=edit_existing_details)
            edit_btn.place(x=10, y=360)


##############################################################################################################################################################################
#----------------------------GUI_WINDOW---------------------------------------------------------------------------------------------------------------------------------------
##############################################################################################################################################################################
    
        root = tk.Toplevel(window)
        root.title('Job Application Tracker')
        root.geometry('1200x550')
        root.resizable(0, 0)

        #Title 
        Label(root, text='JOB APPLICATION TRACKER', font=('Noto Sans CJK TC', 15, 'bold'),bg='mistyrose2').pack(side=TOP, fill=X)

        # Backgrounds and Fonts
        data_entry_frame_bg = 'SkyBlue'
        buttons_frame_bg = 'grey'
        hlb_btn_bg = 'IndianRed'

        AF = font.Font(underline=True)
        lbl_font = ('Georgia', 13)
        entry_font = 'Times 13 bold'
        btn_font = ('Gill Sans MT', 13)

        # StringVar and DoubleVar variables
        com = StringVar()
        pos = StringVar()
        sta = StringVar(value='Applied')

##############################################################################################################################################################################
#----------------------------------FRAMES-------------------------------------------------------------------------------------------------------------------------------------
##############################################################################################################################################################################

        data_entry_frame = Frame(root, bg=data_entry_frame_bg)
        data_entry_frame.place(x=900, y=30, relheight=0.95, relwidth=0.25)
        buttons_frame = Frame(root, bg=buttons_frame_bg)
        buttons_frame.place(relx=0, rely=0.79, relwidth=0.75, relheight=0.21)
        tree_frame = Frame(root)
        tree_frame.place(relx=0, rely=0.05, relwidth=0.75, relheight=0.74)


#######################################################################################################################################################################
#--------------------------DATA_ENTRY_FRAME----------------------------------------------------------------------------------------------------------------------------
#######################################################################################################################################################################

        Label(data_entry_frame, text='JOB DETALIS', font=AF, bg=data_entry_frame_bg).place(x=0, y=5)
        Label(data_entry_frame, text='Date (M/DD/YY) :', font=lbl_font, bg=data_entry_frame_bg).place(x=10, y=60)
        date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
        date.place(x=160, y=60)
        Label(data_entry_frame, text='Company_Name :', font=lbl_font, bg=data_entry_frame_bg).place(x=10, y=110)
        Entry(data_entry_frame, font=entry_font, width=31, text=com).place(x=10, y=140)
        Label(data_entry_frame, text='Job_Position       :', font=lbl_font, bg=data_entry_frame_bg).place(x=10, y=190)
        Entry(data_entry_frame, font=entry_font, width=31, text=pos).place(x=10, y=220)
        Label(data_entry_frame, text='Job_Status          :', font=lbl_font, bg=data_entry_frame_bg).place(x=10, y=275)
        dd1 = OptionMenu(data_entry_frame, sta, *['Applied','Not Applied','Offerd','Rejected','Pending'])
        dd1.place(x=160, y=270)
        dd1.configure(width=10, font=entry_font)

        #SUBMIT_CLEAR_BUTTON
        Button(data_entry_frame, text='SUBMIT', font=btn_font, width=30,bg='palegreen3',command=submit).place(x=10, y=360)
        Button(data_entry_frame, text='CLEAR', font=btn_font, width=30, bg='indianred3',command=clear).place(x=10,y=430)


####################################################################################################################################################################################
#---------------------------BUTTONS_FRAME-------------------------------------------------------------------------------------------------------------------------------------------
####################################################################################################################################################################################
    
        Button(buttons_frame, text='View Details', font=btn_font, width=40, bg='palegreen3',command=view).place(x=500, y=5)
        Button(buttons_frame, text='Delete All', font=btn_font, width=40, bg='indianred3',command=delete_all).place(x=500, y=65)
    
        Button(buttons_frame, text='Edit Details', font=btn_font, width=40, bg='palegreen3',command=edit).place(x=20, y=5)
        Button(buttons_frame, text='Delete Job', font=btn_font, width=40, bg='indianred3',command=delete).place(x=20, y=65)


####################################################################################################################################################################################
#---------------------------TREEVIEW_FRAME------------------------------------------------------------------------------------------------------------------------------------------
####################################################################################################################################################################################

        table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Company_Name','Job_Position','Job_Status'))

        X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
        Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
        X_Scroller.pack(side=BOTTOM, fill=X)
        Y_Scroller.pack(side=RIGHT, fill=Y)

        table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

        table.heading('ID', text='S No.', anchor=CENTER)
        table.heading('Date', text='Date', anchor=CENTER)
        table.heading('Company_Name', text='Company_Name', anchor=CENTER)
        table.heading('Job_Position', text='Job_Position', anchor=CENTER)
        table.heading('Job_Status', text='Job_Status', anchor=CENTER)

        table.column('#0', width=0, stretch=NO)
        table.column('#1', width=60, stretch=NO)
        table.column('#2', width=110, stretch=NO)  # Date column
        table.column('#3', width=350, stretch=NO)  # Payee column
        table.column('#4', width=200, stretch=NO)  # Title column
        table.column('#5', width=160, stretch=NO)  # Amount column

        table.place(relx=0, y=0, relheight=1, relwidth=1)

        list_all()



        # Finalizing the GUI window
        root.update()
        root.mainloop()

    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

        

######################################################################################################################################

    # Close database connection
    db.close()




def new():
    newWindow = tk.Toplevel(window)
    newWindow.title("Signup")
    newWindow.geometry("676x380")

    raw = Image.open(r"C:\Users\fraud\Desktop\Job_Application_Tracker\signup.png")
    bg_img = ImageTk.PhotoImage(raw)
    bg_lab = tk.Label(newWindow, image = bg_img)
    bg_lab.image = bg_img
    bg_lab.pack()
    


    def signup():
        # Create a MySQL connection
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="job_application_tracker"
        )

        # Create a cursor object to interact with the database
        mycursor = mydb.cursor()
        # Get the user input from the entry fields
        username = username_entry.get()
        password = password_entry.get()

        # Insert the user data into the database
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()

        #Dailogue box
        result = mycursor.execute

        if result:
            messagebox.showinfo("SignUp Successful", "Welcome, " + username + " you are Ready To Login!!!")
        else:
            messagebox.showerror("SignUp Failed", "Invalid username or password")
            
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        # Display a success message
        #success_label = tk.Label(newWindow, text="Signup successful!")
        #success_label.pack()


    # Create the username label and entry field
    frame = Frame(newWindow, bg="palegreen3", bd=10, relief="ridge")
    frame.place(relx=0.2, rely=0.5, anchor="center")

    label_sig = Label(frame,text="SignUp",bg ="palegreen3",font=('Noto Sans CJK TC', 40, 'bold'))
    label_sig.pack()
    
    username_label = tk.Label(frame, text="Username:       ",bg ="palegreen3",font=('Courier',16),height=2)
    username_label.pack()
    username_entry = tk.Entry(frame,bg='azure2',font=0,width=18)
    username_entry.pack()

    # Create the password label and entry field
    password_label = tk.Label(frame, text="Password:       ",bg ="palegreen3",font=('Courier',16),height=2)
    password_label.pack()
    password_entry = tk.Entry(frame, show="*",bg='azure2',font=1,width=18)
    password_entry.pack()

    label_empty1 = tk.Label(frame, text="",font=10, bg ="palegreen3",height=1)
    label_empty1.pack()


    # Create the signup button
    signup_button = tk.Button(frame, text="Signup",font=10,bg='orange1', command=signup)
    signup_button.pack(side = LEFT, expand = True, fill = BOTH)


#################################################################

#label_font = font.Font(underline=True)

# Create a frame with a colored background
frame = Frame(window, bg="turquoise1", bd=10, relief="ridge")
frame.place(relx=0.8, rely=0.5, anchor="center")

label_username1 = Label(frame,text="Welcome",bg ="turquoise1",font=('Noto Sans CJK TC', 40, 'bold'))
label_username1.pack()

# Create username label and entry field
label_username = tk.Label(frame, text="USERNAME:        ",font=('Courier',16), bg="turquoise1",height=2)
label_username.pack()
entry_username = tk.Entry(frame,font=0,bg='azure2',width=20)
entry_username.pack()

# Create password label and entry field
label_password = tk.Label(frame, text="PASSWORD:        ",font=('Courier',16), bg ="turquoise1",height=2)
label_password.pack()
entry_password = tk.Entry(frame, show="*",font=1,bg='azure2',width=20)
entry_password.pack()

label_empty = tk.Label(frame, text="",font=10, bg ="turquoise1",height=1)
label_empty.pack()


# Create login button
button_login = tk.Button(frame, text="Login",font=10,bg='palegreen3', command=login)
button_login.pack(side = LEFT, expand = True, fill = BOTH)

# Create the signup button
login_button2 = tk.Button(frame, text="Signup",font=10,bg='orange1', command=new)
login_button2.pack(side = RIGHT, expand = True, fill = BOTH)
# Run the main window loop
window.mainloop()
