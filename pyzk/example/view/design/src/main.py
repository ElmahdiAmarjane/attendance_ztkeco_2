import datetime
import subprocess
from customtkinter import *
import tkinter as tk
from PIL import Image
from tkinter import Canvas
from  .....example.set_user import setup_new_user
from ....database.create_user import create_user  # Adjust this import based on your project structure
from ....database.DbConfig import cursor, conn    # Adjust this import based on your project structure


# Function to execute the live_capture.py script
def start_live_capture():
    subprocess.Popen(["python", "pyzk\\example\\live_capture.py"])

# Initialize the CTk application
app = CTk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculate the width and height for the main view and sidebar
main_view_width = screen_width 
main_view_height = screen_height

# Set the geometry of the application window
app.geometry(f"{screen_width}x{screen_height}")

set_appearance_mode("light")

# Sidebar view function
def sidebar_view():
    sidebar_frame = CTkFrame(master=app, fg_color="#2A8C55", width=screen_width/6, height=screen_height, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    logo_img_data = Image.open("pyzk\\example\\view\\design\\images\\logo.png")
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

    CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    # Example sidebar buttons
    CTkButton(master=sidebar_frame, text="Ajouter nouvel employé", command=create_user_view).pack(anchor="center", pady=(60, 0))
    CTkButton(master=sidebar_frame, text="Historique de présence", command=show_users_view).pack(anchor="center", pady=(16, 0))
    CTkButton(master=sidebar_frame, text="Actual présence", command=live_user_status).pack(anchor="center", pady=(16, 0))
    CTkButton(master=sidebar_frame, text="Dashboard", command=dashborad_stats).pack(anchor="center", pady=(16, 0))

# Show Users view function : HISTORIQUE
def show_users_view():
    def filter_table(event=None):
        search_term = search_entry.get().strip().lower()

        # Clear existing table rows
        for widget in user_table_frame.winfo_children():
            widget.grid_forget()

        # Filter data based on search term
        filtered_data = [row for row in users_data if any(search_term in str(item).lower() for item in row)]

        # Create table headers
        headers = ['ID', 'Name', 'Status', 'Date', 'Time']
        for col, header in enumerate(headers):
            CTkLabel(user_table_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=5, pady=5)

        # Insert filtered data into the table
        for row_idx, row_data in enumerate(filtered_data, start=1):
            employee_id, name, event_type, event_time = row_data
            event_time = str(event_time)
            date, time = event_time.split(' ')[0], event_time.split(' ')[1].split('.')[0]
            
            status_color = "#2A8C55" if event_type.lower() == "in" else "#FF0000"

            CTkLabel(user_table_frame, text=employee_id).grid(row=row_idx, column=0, padx=5, pady=5)
            CTkLabel(user_table_frame, text=name).grid(row=row_idx, column=1, padx=5, pady=5)
            CTkLabel(user_table_frame, text=event_type, text_color=status_color).grid(row=row_idx, column=2, padx=5, pady=5)
            CTkLabel(user_table_frame, text=date).grid(row=row_idx, column=3, padx=5, pady=5)
            CTkLabel(user_table_frame, text=time).grid(row=row_idx, column=4, padx=5, pady=5)

        # Adjust column widths
        user_table_frame.columnconfigure(0, minsize=50)  # Adjust width of column 0
        user_table_frame.columnconfigure(1, minsize=150)  # Adjust width of column 1
        user_table_frame.columnconfigure(2, minsize=100)  # Adjust width of column 2
        user_table_frame.columnconfigure(3, minsize=100)  # Adjust width of column 3
        user_table_frame.columnconfigure(4, minsize=100)  # Adjust width of column 4

    clear_main_view()
    CTkLabel(master=main_view, text="Historique de présence", font=("Arial Bold", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29, 0), padx=27)
    
    # Fetch data from the database
    cursor.execute("""
    SELECT e.employee_id, u.name, e.event_type, e.event_time 
    FROM entry_exit_log e
    INNER JOIN all_users u ON u.id = e.employee_id 
    """)

    users_data = cursor.fetchall()

    # Search input
    search_frame = CTkFrame(master=main_view, fg_color="transparent")
    search_frame.pack(fill="x", padx=20, pady=(20, 10))

    CTkLabel(master=search_frame, text="Search:", font=("Arial", 12)).pack(side="left", padx=(0, 10))
    search_entry = CTkEntry(master=search_frame, fg_color="#F0F0F0", bg_color="#FFFFFF", border_width=1, width=300)
    search_entry.pack(side="left")
    search_entry.bind("<KeyRelease>", filter_table)  # Bind the filter function to key release event

    # Create a frame for the user table with a scrollable canvas
    canvas_frame = CTkFrame(master=main_view)
    canvas_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=(0, 20))

    canvas = Canvas(canvas_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    user_table_frame = CTkFrame(master=canvas)
    canvas.create_window((0, 0), window=user_table_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    user_table_frame.bind("<Configure>", on_frame_configure)

    # Initially show all data
    filter_table()

    # Adjust column widths
    user_table_frame.columnconfigure(0, minsize=50)   # Adjust width of column 0
    user_table_frame.columnconfigure(1, minsize=150)  # Adjust width of column 1
    user_table_frame.columnconfigure(2, minsize=100)  # Adjust width of column 2
    user_table_frame.columnconfigure(3, minsize=100)  # Adjust width of column 3
    user_table_frame.columnconfigure(4, minsize=100)  # Adjust width of column 4
# Create User view function
# def create_user_view():
#     clear_main_view()
#     CTkLabel(master=main_view, text="Ajouter un nouvel employé", font=("Arial Bold", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29, 0), padx=27)
    
#     grid = CTkFrame(master=main_view, fg_color="transparent")
#     grid.pack(fill="both", padx=27, pady=(31, 0))
#     CTkLabel(master=grid, text="Username", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=0, sticky="w")
#     username_entry = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=1, width=300)
#     username_entry.grid(row=1, column=0, ipady=10)
#     CTkLabel(master=grid, text="Telephone", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=2, column=0, sticky="w")
#     tel_entry = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=1, width=300)
#     tel_entry.grid(row=3, column=0, ipady=10)

#     actions = CTkFrame(master=main_view, fg_color="transparent")
#     actions.pack(fill="both")

#     message_label = None  # Variable to track the message label

#     def on_create():
#         nonlocal message_label  # Use the outer variable to track the message label

#         # Clear existing message
#         if message_label is not None:
#             message_label.destroy()

#         username = username_entry.get()
#         telephone = tel_entry.get()
#        # You need to define how to generate or get the UID for the username
#         success = setup_new_user(username,telephone)
#         if success:
#             message_text = "User setup successful!"
#             message_color = "#2A8C55"
#         else:
#             message_text = "User setup failed. Please try again."
#             message_color = "#FF0000"

#         message_label = CTkLabel(master=main_view, text=message_text, font=("Arial Bold", 17), text_color=message_color)
#         message_label.pack(anchor="nw", pady=(10, 0), padx=27)

#     CTkButton(
#         master=actions, 
#         text="Create", 
#         width=300, 
#         font=("Arial Bold", 17), 
#         hover_color="#207244", 
#         fg_color="#2A8C55", 
#         text_color="#fff",
#         command=on_create  # Use the on_create function to handle button click
#     ).pack(side="left", anchor="se", pady=(30, 0), padx=(27, 27))
def create_user_view():
    clear_main_view()
    CTkLabel(master=main_view, text="Ajouter un nouvel employé", font=("Arial Bold", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29, 0), padx=27)
    
    grid = CTkFrame(master=main_view, fg_color="transparent")
    grid.pack(fill="both", padx=27, pady=(31, 0))
    CTkLabel(master=grid, text="Username", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=0, sticky="w")
    username_entry = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=1, width=300)
    username_entry.grid(row=1, column=0, ipady=10)
    CTkLabel(master=grid, text="Telephone", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=2, column=0, sticky="w")
    tel_entry = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=1, width=300)
    tel_entry.grid(row=3, column=0, ipady=10)

    actions = CTkFrame(master=main_view, fg_color="transparent")
    actions.pack(fill="both")

    message_label = None  # Variable to track the message label

    def clear_message():
      nonlocal message_label  # Use the outer variable to track the message label
      if message_label is not None:
        message_label.destroy()
        message_label = None

    def on_create():
     clear_message()

     nonlocal message_label  # Use the outer variable to track the message label

     username = username_entry.get().strip()
     telephone = tel_entry.get().strip()

     if not username:
        message_label = CTkLabel(master=main_view, text="Username cannot be empty.", font=("Arial Bold", 24), text_color="#FF0000")
        message_label.pack(anchor="nw", pady=(10, 0), padx=27)
        return

     processing_label = CTkLabel(master=main_view, text="Processing... Enter your fingerprint", font=("Arial Bold", 24), text_color="#FFA500")
     processing_label.pack(anchor="nw", pady=(10, 0), padx=27)
     main_view.update_idletasks()  # Update the UI to show the processing message

     success = setup_new_user(username, telephone)

     processing_label.destroy()

     if success:
        message_text = "User setup successful!"
        message_color = "#2A8C55"
     else:
        message_text = "User setup failed. Please try again."
        message_color = "#FF0000"

     message_label = CTkLabel(master=main_view, text=message_text, font=("Arial Bold", 20), text_color=message_color)
     message_label.pack(anchor="nw", pady=(10, 0), padx=27)
    CTkButton(
        master=actions, 
        text="Create", 
        width=300, 
        font=("Arial Bold", 17), 
        hover_color="#207244", 
        fg_color="#2A8C55", 
        text_color="#fff",
        command=on_create  # Use the on_create function to handle button click
    ).pack(side="left", anchor="se", pady=(30, 0), padx=(27, 27))

# Dummy function to simulate user setup process

# Show Users view function

def live_user_status():
    clear_main_view()
    CTkLabel(master=main_view, text="Statut actuel de présence", font=("Arial Bold", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29, 0), padx=27)
    
    # Refresh button
    CTkButton(master=main_view, text="Actualiser", command=live_user_status).pack(anchor="ne", padx=20, pady=20)
    
    # Fetch the latest status for each user
    cursor.execute('''
    SELECT
        a.id,
        a.name,
        e.event_type,
        e.event_time
    FROM
        all_users a
    INNER JOIN (
        SELECT
            id,
            employee_id,
            event_type,
            event_time,
            ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY event_time DESC) as rn
        FROM
            entry_exit_log
    ) e ON a.id = e.employee_id
    WHERE
        e.rn = 1;
    ''')

    users_data = cursor.fetchall()

    # Create a frame for the user table with a scrollable canvas
    canvas_frame = CTkFrame(master=main_view)
    canvas_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=20)

    canvas = Canvas(canvas_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    user_table_frame = CTkFrame(master=canvas)
    canvas.create_window((0, 0), window=user_table_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    user_table_frame.bind("<Configure>", on_frame_configure)

    # Create table headers
    headers = ['ID', 'Name', 'Status', 'Date', 'Time']
    for col, header in enumerate(headers):
        CTkLabel(user_table_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=5, pady=5)

    # Insert data into the table
    for row_idx, row_data in enumerate(users_data, start=1):
        employee_id, name, event_type, event_time = row_data
        event_time = str(event_time)
        date, time = event_time.split(' ')[0], event_time.split(' ')[1].split('.')[0]
        
        status_color = "#2A8C55" if event_type.lower() == "in" else "#FF0000"

        CTkLabel(user_table_frame, text=employee_id).grid(row=row_idx, column=0, padx=5, pady=5)
        CTkLabel(user_table_frame, text=name).grid(row=row_idx, column=1, padx=5, pady=5)
        CTkLabel(user_table_frame, text=event_type, text_color=status_color).grid(row=row_idx, column=2, padx=5, pady=5)
        CTkLabel(user_table_frame, text=date).grid(row=row_idx, column=3, padx=5, pady=5)
        CTkLabel(user_table_frame, text=time).grid(row=row_idx, column=4, padx=5, pady=5)
        
        user_table_frame.columnconfigure(0, minsize=50)   # Adjust width of column 0
        user_table_frame.columnconfigure(1, minsize=150)  # Adjust width of column 1
        user_table_frame.columnconfigure(2, minsize=100)  # Adjust width of column 2
        user_table_frame.columnconfigure(3, minsize=100)  # Adjust width of column 3
        user_table_frame.columnconfigure(4, minsize=100)  # Adjust width of column 4

    # Make the scrollbar visible
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to clear the main view
def clear_main_view():
    for widget in main_view.winfo_children():
        widget.destroy()

def dashborad_stats():
    clear_main_view()
    CTkLabel(master=main_view, text="Dashboard", font=("Arial Bold", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29, 0), padx=27)
    
    # 
    cursor.execute('''
       WITH paired_events AS (
          SELECT 
            e1.employee_id,
            DATE(e1.event_time) AS event_date,
            e1.event_time AS entry_time,
            MIN(e2.event_time) AS exit_time
        FROM 
            entry_exit_log e1
        JOIN 
            entry_exit_log e2 
        ON 
            e1.employee_id = e2.employee_id
            AND e1.event_type = 'in'
            AND e2.event_type = 'out'
            AND e2.event_time > e1.event_time
        GROUP BY 
            e1.employee_id, DATE(e1.event_time), e1.event_time
     )
      SELECT 
        employee_id,
        event_date,
        SUM((julianday(exit_time) - julianday(entry_time)) * 24) AS total_hours
     FROM 
        paired_events
     GROUP BY 
        employee_id, event_date
     ORDER BY 
        employee_id, event_date;

        ''')

    users_data_time = cursor.fetchall()
    print("dashboard :")
    for row in users_data_time:
        print("rowrow: ",row)

    # Create a frame for the user table with a scrollable canvas
    canvas_frame = CTkFrame(master=main_view)
    canvas_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=20)

    canvas = Canvas(canvas_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    user_table_frame = CTkFrame(master=canvas)
    canvas.create_window((0, 0), window=user_table_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    user_table_frame.bind("<Configure>", on_frame_configure)

    # Create table headers
    headers = ['ID', 'event date', 'total hours /Day']
    for col, header in enumerate(headers):
        CTkLabel(user_table_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=5, pady=5)

    # Insert data into the table
    for row_idx, row_data in enumerate(users_data_time, start=1):
        employee_id, event_date , total_hours = row_data
         # Convert total_hours to hours and minutes format
        hours = int(total_hours)  # Extract whole hours
        minutes = int((total_hours - hours) * 60)  # Convert remaining decimal to minutes

        # Format the hours and minutes into 'Xh Ymin' format
        formatted_hours_minutes = f'{hours}h {minutes}min'

        CTkLabel(user_table_frame, text=employee_id).grid(row=row_idx, column=0, padx=5, pady=5)
        CTkLabel(user_table_frame, text=event_date).grid(row=row_idx, column=1, padx=5, pady=5)
        CTkLabel(user_table_frame, text=formatted_hours_minutes).grid(row=row_idx, column=2, padx=5, pady=5)
        
        user_table_frame.columnconfigure(0, minsize=50)   # Adjust width of column 0
        user_table_frame.columnconfigure(1, minsize=150)  # Adjust width of column 1
        user_table_frame.columnconfigure(2, minsize=100)  # Adjust width of column 2
        user_table_frame.columnconfigure(3, minsize=100)  # Adjust width of column 3
        user_table_frame.columnconfigure(4, minsize=100)  # Adjust width of column 4
# #######################
#######################       
    
    
    # ######################
     # ######################
     
    CTkLabel(master=main_view, text="STATS BETWEEN TWO DATES (date entered is not considered)", font=("Arial Bold", 16), text_color="#2A8C55").pack(anchor="nw", pady=(5, 0), padx=20)
    # Create a frame for the input fields (fixed frame)
    input_frame = CTkFrame(main_view)
    input_frame.pack(side=tk.TOP, fill=tk.X, pady=(20, 0), padx=27)

    # Create input fields for start_date and end_date in the input frame
    start_date_label = CTkLabel(input_frame, text="Start Date (YYYY-MM-DD):")
    start_date_label.pack(side=tk.LEFT, padx=(0, 10))
    start_date_entry = CTkEntry(input_frame)
    start_date_entry.pack(side=tk.LEFT, padx=(0, 20))

    end_date_label = CTkLabel(input_frame, text="End Date (YYYY-MM-DD):")
    end_date_label.pack(side=tk.LEFT, padx=(0, 10))
    end_date_entry = CTkEntry(input_frame)
    end_date_entry.pack(side=tk.LEFT)
    

    def get_stats():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        # Validate the date inputs
        try:
            # start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            # end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            1==1
        except ValueError:
            result_label.config(text="Invalid date format. Please use YYYY-MM-DD.", text_color="#FF0000")
            return

        # Fetch data from the database
        query = '''
                WITH paired_events AS (
    SELECT 
        e1.employee_id,
        e1.event_time AS entry_time,
        MIN(e2.event_time) AS exit_time
    FROM 
        entry_exit_log e1
    LEFT JOIN 
        entry_exit_log e2 
    ON 
        e1.employee_id = e2.employee_id
        AND e2.event_type = 'out'
        AND e2.event_time > e1.event_time
    WHERE 
        e1.event_type = 'in'
        AND e1.event_time BETWEEN ? AND ?
    GROUP BY 
        e1.employee_id, e1.event_time
)
SELECT 
    employee_id,
    employee_id,
    SUM((julianday(exit_time) - julianday(entry_time)) * 24) AS total_hours
FROM 
    paired_events
WHERE 
    exit_time IS NOT NULL
GROUP BY 
    employee_id
ORDER BY 
    employee_id;


        '''
        cursor.execute(query, (start_date, end_date))
        users_data_time = cursor.fetchall()

        # Clear existing table data
        for widget in user_table_frame.winfo_children():
            widget.destroy()

        # Create table headers
        headers = ['ID', 'Event Date', 'Total Hours/Week']
        for col, header in enumerate(headers):
            CTkLabel(user_table_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=5, pady=5)

        # Insert data into the table
        for row_idx, row_data in enumerate(users_data_time, start=1):
            employee_id, event_date, total_hours = row_data
            # Convert total_hours to hours and minutes format
            hours = int(total_hours)  # Extract whole hours
            minutes = int((total_hours - hours) * 60)  # Convert remaining decimal to minutes

            # Format the hours and minutes into 'Xh Ymin' format
            formatted_hours_minutes = f'{hours}h {minutes}min'


            CTkLabel(user_table_frame, text=employee_id).grid(row=row_idx, column=0, padx=5, pady=5)
            CTkLabel(user_table_frame, text=event_date).grid(row=row_idx, column=1, padx=5, pady=5)
            CTkLabel(user_table_frame, text=formatted_hours_minutes).grid(row=row_idx, column=2, padx=5, pady=5)

        # Adjust column widths
        for col in range(3):
            user_table_frame.columnconfigure(col, minsize=100)

    # Create a button to trigger the get_stats function
    CTkButton(main_view, text="Get Stats", command=get_stats).pack(anchor="nw", pady=(5, 0), padx=27)

    # Create a label to display the result message
    result_label = CTkLabel(main_view, text="Result")
    result_label.pack(anchor="nw", pady=(5, 0), padx=27)

    # Create a frame for the user table with a scrollable canvas
    canvas_frame = CTkFrame(master=main_view)
    canvas_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=20, pady=20)

    canvas = Canvas(canvas_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    user_table_frame = CTkFrame(master=canvas)
    canvas.create_window((0, 0), window=user_table_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    user_table_frame.bind("<Configure>", on_frame_configure)



#######################
########################
  
# Main view frame

main_view = CTkFrame(master=app, fg_color="#fff", width=screen_width-(screen_width/6), height=screen_height, corner_radius=0)
main_view.pack_propagate(0)
main_view.pack(side="right")
scrollbar = CTkScrollbar(main_view, orientation="vertical")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Display the sidebar initially
sidebar_view()
live_user_status()
# Start the live capture process
start_live_capture()
# Start the application main loop
app.mainloop()
