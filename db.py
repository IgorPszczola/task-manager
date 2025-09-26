import sqlite3
from datetime import datetime
from colorama import Fore, init, Style
init()

# conn = sqlite3.connect('to-do.db', check_same_thread=False)
# cursor = conn.cursor()
# conn.row_factory = sqlite3.Row -> instaed of task[1] we can do task["Title"]

def db_init():
    conn = sqlite3.connect('to-do.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        query = '''
                CREATE TABLE IF NOT EXISTS Todo (
                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Title TEXT NOT NULL,
                    Description TEXT NOT NULL,
                    Status TEXT NOT NULL,
                    Created_at DATETIME NOT NULL,
                    Edited_at DATETIME,
                    Deadline DATETIME
                    );
                '''
        cursor.execute(query)
        conn.commit()
    except sqlite3.Error as error:
        print('Failed to create table, error: ', error)
        return None

def get_conn():
    conn = sqlite3.connect('to-do.db', check_same_thread=False)
    return conn


def add_task(title, description, deadline = None):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Todo(Title, Description, Status, Created_at ,Deadline) VALUES (?, ?,?, ?, ?)", (title, description, "Pending",  datetime.now().replace(microsecond=0),deadline))
        print('Task added successfully')
        conn.commit()
    except sqlite3.Error as error:
        print('Failed to add task, error:', error)
        return None
    finally:
        if conn:
            conn.close()


def mark_done(id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Todo SET Status = 'Done' WHERE ID = ?", (id,))
        print('Task marked done')
        conn.commit()
    except sqlite3.Error as error:
        print('Failed to mark task, error:', error)
        return None
    finally:
        if conn:
            conn.close()


# def list_all_tasks(order_by = None):
#     try:
#         if not order_by:
#             data = cursor.execute("SELECT * FROM Todo")
#             print_rows(data)
#         elif order_by == "Title":
#             data = cursor.execute("SELECT * FROM Todo ORDER BY Title")
#             print_rows(data)
#         elif order_by == "Description":
#             data = cursor.execute("SELECT * FROM Todo ORDER BY Description")
#             print_rows(data)
#         elif order_by == "Created_at":
#             data = cursor.execute("SELECT * FROM Todo ORDER BY Created_at")
#             print_rows(data)
#         elif order_by == "Deadline":
#             data = cursor.execute("SELECT * FROM Todo ORDER BY Deadline")
#             print_rows(data)
#
#         conn.commit()
#
#     except sqlite3.Error as error:
#         print('Failed to list all tasks, error: ', error)


# def print_deadline_of_task(id):
#     try:
#         data = cursor.execute("SELECT Deadline FROM Todo WHERE Id = ?" , (id,))
#         date = data.fetchone()
#         date = datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S')
#         task = cursor.execute("SELECT Title FROM Todo WHERE Id = ?", (id,))
#         task = task.fetchone()
#         # fetchone -> returns tuple
#         # fetchall -> returns dictionary
#         print(f"Task '{task[0]}' has a deadline of {date}")
#         conn.commit()
#     except sqlite3.Error as error:
#         print('Failed to print deadline of task, error: ', error)


def delete_task(id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Todo WHERE Id = ?", (id,))
        print(f'Task with id = {id} deleted')
        conn.commit()
    except sqlite3.Error as error:
        print('Failed to delete task, error: ', error)
        return None
    finally:
        if conn:
            conn.close()


def check_deadline():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        data = cursor.execute("SELECT * FROM Todo WHERE Status = 'Pending'")
        for row in data.fetchall():
            if row[6]:
                deadline = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
                if deadline < datetime.now():
                    cursor.execute("UPDATE Todo SET Status = 'Pending(Late)' WHERE Id = ?", (row[0], ))
        conn.commit()
    except sqlite3.Error as error:
        print('Failed to check deadline, error: ', error)
        return None
    finally:
        if conn:
            conn.close()


def check_is_correct_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        data = cursor.execute("SELECT * FROM Todo WHERE ID = ?", (id, ))
        data = data.fetchone()
        if data is None:
            return False
        conn.commit()
        return True
    except sqlite3.Error as error:
        print('Failed to check task, error: ', error)
        return None
    finally:
        if conn:
            conn.close()



# def print_rows(data):
#     for row in data.fetchall():
#         if row[3] == 'Pending':
#             color = Fore.YELLOW
#         elif row[3] == 'Pending(Late)':
#             color = Fore.RED
#         else:
#             color = Fore.GREEN
#         print(f"ID = {row[0]}\n"
#             f"Title = {row[1]}\n"
#             f"Description = {row[2]}\n"
#             f"Status = {color + row[3]}{Style.RESET_ALL}\n"
#             f"Created_at = {row[4]}\n"
#             f"Edited_at = {row[6]}\n"
#             f"Deadline = {row[5]}\n")


def list_not_done():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Todo WHERE Status = 'Pending' OR Status = 'Pending(Late)'")
        data = cursor.fetchall()
        return data
        # print_rows(data)
    except sqlite3.Error as error:
        print('Failed to list not done tasks, error: ', error)
        return []
    finally:
        if conn:
            conn.close()

def parse_deadline(deadline):
    if not deadline:
        return None
    try:
        return datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def delete_done():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        data = cursor.execute("SELECT * FROM Todo WHERE Status = 'Done'")
        data = data.fetchall()
        for row in data:
            id_ = row[0]
            cursor.execute("DELETE FROM Todo WHERE Id = ?", (id_,))
            conn.commit()
    except sqlite3.Error as error:
        print('Failed to delete done tasks, error: ', error)
        return None
    finally:
        if conn:
            conn.close()

def edit_task(edited_id, Title, Description, Deadline):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        # allowerd_columns = ["Title", "Description", "Status", "Deadline"]
        # if edited_column not in allowerd_columns:
        #     print("Incorrect column to edit")
        #     return

        query = f"UPDATE Todo SET Title = ?, Description = ?, Deadline = ? WHERE ID = ?"
        cursor.execute(query, (Title, Description, Deadline, edited_id))
        cursor.execute("UPDATE Todo SET Edited_at = ? WHERE ID = ?", (datetime.now().replace(microsecond=0),edited_id))
        conn.commit()
        print(f"Task with ID = {edited_id} edited successfully")
    except sqlite3.Error as error:
        print('Failed to edit task, error: ', error)
        return None
    finally:
        if conn:
            conn.close()


def fetch_all_tasks():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Todo")
        data = cursor.fetchall()
        if data:
            return data
        else:
            return None
    except sqlite3.Error as error:
        print('Failed to fetch tasks, error: ', error)
        return []
    finally:
        if conn:
            conn.close()


def tasks_before_deadline():
    conn = get_conn()
    cursor = conn.cursor()
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        data =  cursor.execute("SELECT * FROM Todo WHERE Deadline > ?", (current_time_str,))
        data = data.fetchall()
        if data:
            return data
        else:
            return None
    except sqlite3.Error as error:
        print('Failed to fetch tasks, error: ', error)
        return []
    finally:
        if conn:
            conn.close()




