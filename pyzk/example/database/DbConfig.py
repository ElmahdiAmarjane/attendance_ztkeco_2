import sqlite3
import datetime
# Connect to SQLite database (it will be created if it does not exist)
conn = sqlite3.connect('attendance.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()


# SQL statement to create the 'all_users' table
create_all_users_table = '''
CREATE TABLE IF NOT EXISTS all_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    template BLOB,
    telephone TEXT
)
'''
drop_all_users_table = '''
DROP table all_users ;
'''
#cursor.execute(drop_all_users_table)

# SQL statement to create the 'attendance_details' table
create_entry_exit_log_table = '''
CREATE TABLE IF NOT EXISTS entry_exit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

'''

# Execute the SQL statements
cursor.execute(create_all_users_table)
cursor.execute(create_entry_exit_log_table)
########################
# Insert a user into the 'all_users' table
insert_user = '''
INSERT INTO all_users (name,telephone) VALUES (?,?)
'''
# user_name = 'ahmedtest'
# cursor.execute(insert_user, (user_name,))

select_user = '''
    SELECT * FROM all_users
'''
#cursor.execute(select_user)
results = cursor.fetchall()
print(results)

# Commit the changes
conn.commit()

def get_user_by_username(username):
    try:
        # Execute the query
        cursor.execute("SELECT * FROM all_users WHERE name=?", (username,))
        user = cursor.fetchone()  # fetchone() retrieves the first row found

        return user  # Return the user if found, otherwise None

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

# Close the connection
#conn.close()
def get_last_event_type(employee_id):
    try:

        # Query the last recorded event type for the employee
        cursor.execute("SELECT event_type FROM entry_exit_log WHERE employee_id=? ORDER BY event_time DESC LIMIT 1", (employee_id,))
        last_event = cursor.fetchone()
        if last_event:
            return last_event[0]  # Return the event type ('getin' or 'getout')
        else:
            return 'in'  # Return None if no event found

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    
def log_entry_exit(attendance):
    try:
# Determine event_type based on the last event type retrieved
        if attendance.punch == 0 or attendance.punch==4: # 4 and 0 for breakin and Arrivee
            event_type = 'in'
        elif attendance.punch==1 or attendance.punch==5: # 5 and 1 for breakout and Depart
           event_type = 'out'

        print("eventtype : ",attendance.punch)
        print("attendace time type : ",type(attendance.get_time()))
        cursor.execute("INSERT INTO entry_exit_log (employee_id, event_type, event_time) VALUES (?, ?, ?)",
                       (attendance.get_id(), event_type, attendance.get_time()))
        conn.commit()

        print(f"Successfully logged {event_type} for employee ID {attendance.get_id()}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    
def update_template_for_user(uid,template):

    try:
        

        # Update the template in the SQLite database
        cursor.execute("UPDATE all_users SET  template = ? WHERE id = ?",
                       (template, uid))
        
        conn.commit()  # Commit the transaction
        print(f"Fingerprint template updated successfully for user ID {uid}")

    except Exception as e:
        print(f"Failed to update fingerprint template for user ID {uid}: {e}")

select_user = '''
    SELECT * FROM all_users
'''
cursor.execute(select_user)
results = cursor.fetchall()

print("🟢USERS : ",results)

def delete_users_without_fingerprint():
    try:
        # Query the last recorded event type for the employee
        cursor.execute("DELETE FROM all_users where template IS NULL")
        print("DELETE USER THAT NOT HAVE FINGERPRINT✅")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        

#print("Database and tables created successfully.")
