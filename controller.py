import mysql.connector
import os
import matplotlib.pyplot as pt

# Configurations
from config import config
from dotenv import load_dotenv
from pyzk.example.set_user import setup_new_employee
load_dotenv()  # Imports environemnt variables from the '.env' file

# ===================SQL Connectivity=================

# SQL Connection
connection = mysql.connector.connect(
    host=config.get("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=config.get("DB_NAME"),
    port="3306",
    autocommit=config.get("DB_AUTOCOMMIT"),
)

cursor = connection.cursor(buffered=True)

# SQL functions


def checkUser(username, password=None):
    cmd = f"Select count(username) from login where username='{username}' and BINARY password='{password}'"
    cursor.execute(cmd)
    cmd = None
    a = cursor.fetchone()[0] >= 1
    return a


def count_all_employees():
    cmd = "SELECT count(*) FROM employees"
    cursor.execute(cmd)
    cmd=None
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def count_in_employees():
    cmd = ''' SELECT COUNT(*) AS num_in
           FROM (
              SELECT employee_id, event_type
              FROM entry_exit_log
            WHERE event_time = (
            SELECT MAX(event_time)
            FROM entry_exit_log AS sub
            WHERE sub.employee_id = entry_exit_log.employee_id
            )
           ) AS latest_events
            WHERE event_type = 'in';
        '''
    cursor.execute(cmd)
    cmd=None
    return cursor.fetchone()
def count_out_employees():
    cmd = ''' SELECT COUNT(*) AS num_in
           FROM (
              SELECT employee_id, event_type
              FROM entry_exit_log
            WHERE event_time = (
            SELECT MAX(event_time)
            FROM entry_exit_log AS sub
            WHERE sub.employee_id = entry_exit_log.employee_id
            )
           ) AS latest_events
            WHERE event_type = 'out';
        '''
    cursor.execute(cmd)
    cmd=None
    return cursor.fetchone()

def log_entry_exit(attendance):
    try:
        # Determine event_type based on the last event type retrieved
        if attendance.punch == 0 or attendance.punch == 4:  # 4 and 0 for breakin and Arrivee
            event_type = 'in'
        elif attendance.punch == 1 or attendance.punch == 5:  # 5 and 1 for breakout and Depart
            event_type = 'out'

        print("eventtype : ", attendance.punch)
        print("attendance time type : ", type(attendance.get_time()))

        cursor.execute("INSERT INTO entry_exit_log (employee_id, event_type, event_time) VALUES (%s, %s, %s)",
                       (attendance.get_id(), event_type, attendance.get_time()))

        print(f"Successfully logged {event_type} for employee ID {attendance.get_id()}")

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")


def update_template_for_employee(uid, template):
    try:
        # Update the template in the MySQL database
        cursor.execute("UPDATE employees SET template = %s WHERE id = %s", (template, uid))

        
        print(f"Fingerprint template updated successfully for user ID {uid}")

    except mysql.connector.Error as e:
        print(f"Failed to update fingerprint template for user ID {uid}: {e}")


def  insert_employee(employeename,telephone):

    try:

        # Update the template in the SQLite database
        cursor.execute("INSERT INTO employees (name_, telephone) VALUES (%s, %s)",
                        (employeename, telephone))
        print("✅ INSERTED EMPLOYEE SUCCESS.")

    except Exception as e:
        print(f"❌Failed to Insert EMPLOYEE SUCCESS.: {e}")

def delete_employees_without_fingerprint():
    try:
        # Query the last recorded event type for the employee
        cursor.execute("DELETE FROM employees where template IS NULL")
        print("DELETE USER THAT NOT HAVE FINGERPRINT✅")
    except mysql.connector.Error as e:
        print(f"MySql error: {e}")
    
def get_employee_by_username(username):
    try:
        # Execute the queryg
        print("USERNAME ::: ",username)
        cursor.execute("SELECT * FROM employees WHERE name_=%s", (username,))
        user = cursor.fetchone()  # fetchone() retrieves the first row found
        print("USER CCC  : ",user)
        return user  # Return the user if found, otherwise None

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")
        return None

    
def create_employee(username_entry,telephone):
        print(username_entry,telephone)
        try:
         insert_employee(username_entry,telephone)
         user = get_employee_by_username(username_entry)
         print("✅USER CREATEED INFO : ",user)
         return user  
        except mysql.connector.Error as e:
            print("MySQL error : ",e) 
# for database local and device 
def create_new_employee(username,telephone):
     return setup_new_employee(username,telephone)

def get_employees_with_average_hours():
    query = """
    WITH DailyHours AS (
        SELECT 
            e.id AS employee_id,
            e.name_,
            DATE(l_in.event_time) AS work_date,
            TIMESTAMPDIFF(SECOND, l_in.event_time, l_out.event_time) / 3600 AS hours_worked
        FROM 
            employees e
        JOIN 
            entry_exit_log l_in ON e.id = l_in.employee_id AND l_in.event_type = 'in'
        JOIN 
            entry_exit_log l_out ON e.id = l_out.employee_id AND l_out.event_type = 'out'
        WHERE 
            l_in.event_time < l_out.event_time
    ),
    EmployeeWorkSummary AS (
        SELECT 
            employee_id,
            name_,
            SUM(hours_worked) AS total_hours_worked,
            COUNT(DISTINCT work_date) AS days_worked
        FROM 
            DailyHours
        GROUP BY 
            employee_id, name_
    )
    SELECT 
        employee_id,
        name_,
        total_hours_worked,
        days_worked,
        total_hours_worked / days_worked AS avg_hours_per_day
    FROM 
        EmployeeWorkSummary
    WHERE 
        total_hours_worked / days_worked >= 8;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    nbremployeesmore = cursor.rowcount
    return results,nbremployeesmore

def get_employees_with_less_than_8_hours():
    query = """
    WITH DailyHours AS (
        SELECT 
            e.id AS employee_id,
            e.name_,
            DATE(l_in.event_time) AS work_date,
            TIMESTAMPDIFF(SECOND, l_in.event_time, l_out.event_time) / 3600 AS hours_worked
        FROM 
            employees e
        JOIN 
            entry_exit_log l_in ON e.id = l_in.employee_id AND l_in.event_type = 'in'
        JOIN 
            entry_exit_log l_out ON e.id = l_out.employee_id AND l_out.event_type = 'out'
        WHERE 
            l_in.event_time < l_out.event_time
    ),
    EmployeeWorkSummary AS (
        SELECT 
            employee_id,
            name_,
            SUM(hours_worked) AS total_hours_worked,
            COUNT(DISTINCT work_date) AS days_worked
        FROM 
            DailyHours
        GROUP BY 
            employee_id, name_
    )
    SELECT 
        employee_id,
        name_,
        total_hours_worked,
        days_worked,
        total_hours_worked / days_worked AS avg_hours_per_day
    FROM 
        EmployeeWorkSummary
    WHERE 
        total_hours_worked / days_worked < 8;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    nbremployeesless = cursor.rowcount
    return results, nbremployeesless

def get_in_employees():
    cmd = '''
        SELECT e.id as id , e.name_ as id , e.telephone as Telephone , latest_events.event_time as event_time
        FROM employees e
        JOIN (
            SELECT employee_id, event_type, event_time
            FROM entry_exit_log
            WHERE event_time = (
                SELECT MAX(event_time)
                FROM entry_exit_log AS sub
                WHERE sub.employee_id = entry_exit_log.employee_id
            )
        ) AS latest_events
        ON e.id = latest_events.employee_id
        WHERE latest_events.event_type = 'in';
    '''
    cursor.execute(cmd)
    return cursor.fetchall()


def get_out_employees():
    cmd = '''
        SELECT e.id as id , e.name_ as name, e.telephone as Telephone ,latest_events.event_time as event_time
        FROM employees e
        JOIN (
            SELECT employee_id, event_type, event_time
            FROM entry_exit_log
            WHERE event_time = (
                SELECT MAX(event_time)
                FROM entry_exit_log AS sub
                WHERE sub.employee_id = entry_exit_log.employee_id
            )
        ) AS latest_events
        ON e.id = latest_events.employee_id
        WHERE latest_events.event_type = 'out';
    '''
    cursor.execute(cmd)
    return cursor.fetchall()


def get_all_employees():
    cmd = "SELECT id , name_ as name , telephone , created_at FROM employees"
    cursor.execute(cmd)
    cmd=None
    return cursor.fetchall()


def get_total_hours_worked():
    cmd = '''
        SELECT SUM(TIMESTAMPDIFF(HOUR, in_time, out_time)) AS total_hours_worked
        FROM (
            SELECT employee_id,
                   MIN(event_time) AS in_time,
                   MAX(event_time) AS out_time
            FROM entry_exit_log
            WHERE event_type IN ('in', 'out')
            GROUP BY employee_id, DATE(event_time)
            HAVING COUNT(DISTINCT event_type) = 2
        ) AS daily_work_hours;
    '''
    cursor.execute(cmd)
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def get_average_total_hours_per_employee():
    total_hours_worked = get_total_hours_worked()
    total_employees = count_all_employees()
    
    if total_employees == 0:
        return 0
    average_hours = float(total_hours_worked) / total_employees
    return  convert_hours_to_readable_format(average_hours)

def convert_hours_to_readable_format(hours):
    hours_in_a_day = 24
    days_in_a_month = 30
    days_in_a_year = 365

    # Convert hours to days, months, and years
    days = hours / hours_in_a_day
    months = days / days_in_a_month
    years = days / days_in_a_year

    # Find the largest non-zero unit to display
    if years >= 1:
        result = f"{years:.2f} y"
    elif months >= 1:
        result = f"{months:.2f} m"
    elif days >= 1:
        result = f"{days:.2f} d"
    else:
        result = f"{hours:.2f} h"

    return result


def delete_employee(employee_id):
    cmd = "DELETE FROM EMPLOYEES WHERE id = %s"
    try:
        cursor.execute(cmd, (employee_id,))
        # Commit changes to the database
        connection.commit()
        # Check if any row was affected
        if cursor.rowcount == 0:
            return False
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def get_employee_by_id(employee_id):
    cmd = "SELECT id, name_, telephone, created_at FROM employees WHERE id = %s"
    cursor.execute(cmd, (employee_id,))
    result = cursor.fetchone()
    if result:
        # Assuming result is a tuple in the order: (id, name, telephone, created_at)
        return {
            'id': result[0],
            'name': result[1],
            'telephone': result[2],
            'created_at': result[3]
        }
    return None

# In your controller module (controller.py)

def update_employee(name, telephone, id):
    cmd = """
    UPDATE employees
    SET name_ = %s, telephone = %s
    WHERE id = %s
    """
    cursor.execute(cmd, (name, telephone, id))
    if cursor.rowcount == 0:
        return False
    return True






# def human_format(num):
#     if num < 1000:
#         return num

#     magnitude = 0
#     while abs(num) >= 1000:
#         magnitude += 1
#         num /= 1000
#     return "%.1f%s" % (num, ["", "K", "M", "G", "T", "P"][magnitude])


# def updatePassword(username, sec_ans, sec_que, password):
#     cmd = f"update login set password='{password}' where username='{username}' and sec_ans='{sec_ans}' and sec_que='{sec_que}' limit 1;"
#     cursor.execute(cmd)
#     cmd = f"select count(username) from login where username='{username}' and password='{password}' and sec_ans='{sec_ans}' and sec_que='{sec_que}';"
#     cursor.execute(cmd)
#     return cursor.fetchone()[0] >= 1


# def updateUsername(oldusername, password, newusername):
#     cmd = f"update login set username='{newusername}' where username='{oldusername}' and password='{password}' limit 1;"
#     cursor.execute(cmd)
#     cmd = f"select count(username) from login where username='{newusername}' and password='{password}''"
#     cursor.execute(cmd)
#     return cursor.fetchone()[0] >= 1



# def find_g_id(name):
#     cmd = f"select g_id from guests where name = '{name}'"
#     cursor.execute(cmd)
#     out = cursor.fetchone()[0]
#     return out


# def checkin(g_id):
#     cmd = f"select * from reservations where g_id = '{g_id}';"
#     cursor.execute(cmd)
#     reservation = cursor.fetchall()
#     if reservation != []:
#         subcmd = f"update reservations set check_in = curdate() where g_id = '{g_id}' "
#         cursor.execute(subcmd)
#         return "successful"
#     else:
#         return "No reservations for the given Guest"



# def checkout(id):
#     cmd = f"update reservations set check_out=current_timestamp where id={id} limit 1;"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# # ============Python Functions==========


# def acceptable(*args, acceptables):
#     """
#     If the characters in StringVars passed as arguments are in acceptables return True, else returns False
#     """
#     for arg in args:
#         for char in arg:
#             if char.lower() not in acceptables:
#                 return False
#     return True



# # Get all guests
# def get_guests():
#     cmd = "select id, name, address, email_id, phone, created_at from guests;"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return cursor.fetchall()


# # Add a guest
# def add_guest(name, address, email_id, phone):
#     cmd = f"insert into guests(name,address,email_id,phone) values('{name}','{address}','{email_id}',{phone});"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# # add a room
# def add_room(room_no, price, room_type):
#     cmd = f"insert into rooms(room_no,price,room_type) values('{room_no}',{price},'{room_type}');"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# # Get All rooms
# def get_rooms():
#     cmd = "select id, room_no, room_type, price, created_at from rooms;"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return cursor.fetchall()


# # Get all reservations
# def get_reservations():
#     cmd = "select id, g_id, r_id, check_in, check_out, meal from reservations;"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return cursor.fetchall()


# # Add a reservation
# def add_reservation(g_id, meal, r_id, check_in="now"):
#     cmd = f"insert into reservations(g_id,check_in,r_id, meal) values('{g_id}',{f'{chr(39) + check_in + chr(39)}' if check_in != 'now' else 'current_timestamp'},'{meal}','{r_id}');"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# # Get all room count
# def get_total_rooms():
#     cmd = "select count(room_no) from rooms;"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return cursor.fetchone()[0]


# # Check if a room is vacant
# def booked():
#     cmd = f"select count(ros.id) from reservations rs, rooms ros where rs.r_id = ros.id and rs.check_out is Null;"
#     cursor.execute(cmd)

#     return cursor.fetchone()[0]


# def vacant():
#     return get_total_rooms() - booked()


# def bookings():
#     cmd = f"select count(rs.id) from reservations rs , rooms ros where rs.r_id = ros.id and ros.room_type = 'D';"
#     cursor.execute(cmd)
#     deluxe = cursor.fetchone()[0]

#     cmd1 = f"select count(rs.id) from reservations rs , rooms ros where rs.r_id = ros.id and ros.room_type = 'N';"
#     cursor.execute(cmd1)
#     Normal = cursor.fetchone()[0]

#     return [deluxe, Normal]


# # Get total hotel value
# def get_total_hotel_value():
#     cmd = "select sum(price) from rooms;"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     value = cursor.fetchone()[0]

#     return human_format(value)


# def delete_reservation(id):
#     cmd = f"delete from reservations where id='{id}';"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# def delete_room(id):
#     cmd = f"delete from rooms where id='{id}';"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# def delete_guest(id):
#     cmd = f"delete from guests where id='{id}';"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# def update_rooms(id, room_no, room_type, price):
#     cmd = f"update rooms set room_type = '{room_type}',price= {price}, room_no = {room_no} where id = {id};"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# def update_guests(name, address, id, phone):

#     cmd = f"update guests set address = '{address}',phone = {phone} , name = '{name}' where id = {id};"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# def update_reservations(
#     g_id, check_in, room_id, reservation_date, check_out, meal, type, id
# ):
#     cmd = f"update reservations set check_in = '{check_in}',check_out = '{check_out}',g_id = {g_id}, \
#         r_date = '{reservation_date}',meal = {meal},r_type='{type}', r_id = {room_id} where id= {id};"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True


# def meals():
#     cmd = f"select sum(meal) from reservations;"
#     cursor.execute(cmd)
#     meals = cursor.fetchone()[0]

#     return human_format(meals)


# def update_reservation(id, g_id, check_in, room_id, check_out, meal):
#     cmd = f"update reservations set check_in = '{check_in}', check_out = '{check_out}', g_id = {g_id}, meal = '{meal}', r_id = '{room_id}' where id= '{id}';"
#     cursor.execute(cmd)
#     if cursor.rowcount == 0:
#         return False
#     return True
