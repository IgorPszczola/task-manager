import sqlite3


def fix_deadlines():
    conn = sqlite3.connect("to-do.db")
    cursor = conn.cursor()

    cursor.execute("SELECT ID, Deadline FROM Todo")
    rows = cursor.fetchall()

    for r in rows:
        task_id, deadline = r
        if deadline is not None:
            try:
                from datetime import datetime
                datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
            except Exception:
                print(f"❌ Invalid deadline in record ID={task_id}: {deadline} -> setting to NULL")
                cursor.execute("UPDATE Todo SET Deadline = NULL WHERE ID = ?", (task_id,))

    conn.commit()
    conn.close()
    print("✅ Fix completed.")


if __name__ == "__main__":
    fix_deadlines()