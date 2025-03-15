import sqlite3
import os

def delete_employer_account(employer_id):  
    conn, cursor = connection()
    if conn is None:
        return None
    try:
        query = "SELECT employee_name, employee_password, employee_email FROM Employee WHERE employee_id = ?"
        cursor.execute("DELETE FROM Employer WHERE employer_id = ?", (employer_id,))  
        conn.commit() 
        if cursor.rowcount == 0:  
            print(f"No employer found with employer_id: {employer_id}")  
        else:  
            print(f"Employer account with employer_id: {employer_id} has been deleted.") 
    except sqlite3.Error as e:  
        print(f"An error occurred: {e}")
    

def get_employee_details(employee_id):
        # Function to retrieve employee details from the database
        conn, cursor = connection()
        if conn is None:
            return None

        try:
            query = "SELECT employee_name, employee_password, employee_email FROM Employee WHERE employee_id = ?"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            return result if result else ("", "", "")  # Return empty if no data found
        except Exception as e:
            print(f"Error retrieving employee details: {e}")
            return "", "", ""
        finally:
            close_connection(conn)
# Database connection functions
def connection():
    pathdb = r"C:\Users\Shema\Desktop\version1.0\database\CareerCastle.db"
    try:
        if os.path.exists(pathdb):
            conn = sqlite3.connect(pathdb)
            cursor = conn.cursor()
            print("Connection established")
        else:
            print("Path not found")
            return None, None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None, None

    return conn, cursor

def close_connection(conn):
    if conn:
        conn.close()
        print("Connection closed")

# Function to retrieve employer passwords
def retrieve_employers_password(employer_name):
    conn, cursor = connection()
    if conn is None:
        return None
    try:
        query = "SELECT employer_password FROM Employer WHERE employer_name = ?"
        cursor.execute(query, (employer_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error retrieving employer password: {e}")
        return None
    finally:
        close_connection(conn)

# Function to retrieve employee passwords
def retrieve_employees_password(employee_name):
    conn, cursor = connection()
    if conn is None:
        return None
    try:
        query = "SELECT employee_password FROM Employee WHERE employee_name = ?"
        cursor.execute(query, (employee_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error retrieving employee password: {e}")
        return None
    finally:
        close_connection(conn)

# Function to retrieve employer IDs
def retrieve_employers_id(employer_name):
    conn, cursor = connection()
    if conn is None:
        return None
    try:
        query = "SELECT employer_id FROM Employer WHERE employer_name = ?"
        cursor.execute(query, (employer_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error retrieving employer ID: {e}")
        return None
    finally:
        close_connection(conn)

def get_user_jobs(user_id, job_type='posted'):
    """
    Fetch jobs based on user_id and job type (posted/offered).
    """
    conn = sqlite3.connect("your_database.db")  # Adjust your database connection string
    cursor = conn.cursor()

    if job_type == 'posted':
        cursor.execute("SELECT job_title, job_nature FROM job WHERE posted_by = ?", (user_id,))
    elif job_type == 'offered':
        cursor.execute("SELECT job_title, job_nature FROM job WHERE offered_to = ?", (user_id,))

    jobs = cursor.fetchall()
    conn.close()
    return jobs

def update_employee(name, password, email, employee_id):
    conn, cursor = connection()
    try:
        query = """UPDATE Employee
                   SET employee_name = ?, employee_password = ?, employee_email = ?
                   WHERE employee_id = ?"""
        cursor.execute(query, (name, password, email,employee_id))
        conn.commit()
        print("Employee details updated successfully")
    except Exception as e:
        print(f"Error updating employee details: {e}")
    
        close_connection(conn)
    

def insert_employee(name, password, email):
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute("INSERT INTO Employee (employee_name, employee_password, employee_email) VALUES (?, ?, ?)",
                   (name, password, email))
    conn.commit()
    print("Employee inserted successfully")
    close_connection(conn)

def insert_employer(name, password, email):
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute("INSERT INTO Employer (employer_name, employer_password, employer_email) VALUES (?, ?, ?)",
                   (name, password, email))
    conn.commit()
    print("Employer inserted successfully")
    close_connection(conn)


# Function to retrieve employee IDs
def retrieve_employees_id(employee_name):
    conn, cursor = connection()
    if conn is None:
        return None
    try:
        query = "SELECT employee_id FROM Employee WHERE employee_name = ?"
        cursor.execute(query, (employee_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error retrieving employee ID: {e}")
        return None
    finally:
        close_connection(conn)

# Other existing functions
def retrieve_employers():
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute("SELECT * FROM Employer")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    close_connection(conn)
    return rows

def retrieve_application():
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute("""SELECT employee_name,education_level,experience,employer_name,job_title,job_nature,state 
                   FROM employee NATURAL join Job_application
                        JOIN Job_posting USING(job_posting_id)
                        join Employer using (employer_id)
                        join job using (job_id)
                        """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    close_connection(conn)
    return rows

def retrieve_employed():
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute("""  select employee_name,job_title,job_nature
                        from employee NATURAL join Job_application
                        	JOIN Job_posting USING(job_posting_id)
                        	join Employer using (employer_id)
                        	join job using (job_id)
                        WHERE state like "approve"
                        """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    close_connection(conn)
    return rows

def retrieve_employers2(employer_id):
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute(f"SELECT * FROM Employer WHERE employer_id = ?",(employer_id,))
    row = cursor.fetchone()
    close_connection(conn)
    return row

def retrieve_employees():
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute("SELECT * FROM Employee")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    close_connection(conn)
    return rows

def retrieve_jobs():
    conn, cursor = connection()
    if conn is None:
        return

    cursor.execute("SELECT * FROM Job")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    close_connection(conn)
    return rows
