import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a database connection to SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect("tasks.db")
        print(f"Connected to SQLite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table():
    """Create a sample users table"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        
        # Create table query
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT,
            description TEXT,
            location TEXT,
            price FLOAT,
            taskowner TEXT,
            isStarted BOOL,
            isCompleted BOOL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        
        cursor.execute(create_table_query)
        conn.commit()
        print("Table created successfully")
        
    except Error as e:
        print(f"Error creating table: {e}")

def add_task(task):
    conn = create_connection()
    sql = '''INSERT INTO tasks(username, name, description, location, price, isStarted)
             VALUES(?, ?, ?, ?, ?, ?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, task)
        conn.commit()
        print(f"Successfully inserted task with ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"Error inserting task: {e}")
        return None
   

def get_inactive_tasks():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        
        # Create table query
        create_table_query =  '''
            SELECT * FROM tasks 
            WHERE isStarted IS NULL 
            OR isStarted = 0 
            OR isStarted = 'false'
            '''
        cursor.execute(create_table_query)
        resp = cursor.fetchall()
        conn.commit()
        print(resp)
        if resp == []:
            return []
        else:
            return resp
        
    except Error as e:
        print(f"Error creating table: {e}")
    

def accept_task(id,taskowner):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        
        update_query = '''
            UPDATE tasks 
            SET taskowner = ?,
                isStarted = 'True'
            WHERE id = ?
            '''
        
        task_data = (taskowner,id)
        cursor.execute(update_query, task_data)
        conn.commit()
        print("task accepted")
        return True
        
    except Error as e:
        print(f"Error creating table: {e}")

def get_accepted_tasks(user):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE taskowner = ?", (user,))
        resp = cursor.fetchall()
        conn.commit()
        return resp
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        return []
    finally:
        conn.close()