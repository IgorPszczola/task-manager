# from db import add_task, mark_done, list_all_tasks, print_deadline_of_task, delete_task, check_deadline, check_is_correct_id, list_not_done
from db import *
import sys
from datetime import datetime

if __name__ == '__main__':
    check_deadline()
    if not len(sys.argv) > 1:
        print("Please write command")

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 4:
            print("Not enough arguments to add task")
            sys.exit(0)
        title = sys.argv[2]
        if not title.strip():
            print("Please enter a correct title")
            sys.exit(1)

        description = sys.argv[3]
        if not description.strip():
            print("Please enter a correct description")
            sys.exit(1)
        deadline = None
        if len(sys.argv) > 4:
            deadline = sys.argv[4]
            try:
                deadline = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print("Please enter a valid deadline (Y-m-d)")
                sys.exit(1)
        add_task(title, description, deadline)
    elif command == 'list':
        if len(sys.argv) == 2:
            list_all_tasks()
        elif len(sys.argv) == 3:
            list_all_tasks(sys.argv[2])
    elif command == 'deadline':
        if len(sys.argv) < 3:
            print("Please enter ID of wanted task")
            sys.exit(1)
        try:
            id_ = int(sys.argv[2])
            if check_is_correct_id(id_) is False:
                print("No record with that ID")
                sys.exit(1)
        except ValueError:
            print("Please enter correct ID of wanted task")
            sys.exit(1)
        else:
            print_deadline_of_task(id_)
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Please enter ID of task, which will be deleted")
            sys.exit(1)
        try:
            id_ = int(sys.argv[2])
            if check_is_correct_id(id_) is False:
                print("No record with that ID")
                sys.exit(1)
        except ValueError:
            print("Please enter correct ID of task, which will be deleted")
            sys.exit(1)
        else:
            delete_task(id_)
    elif command == 'mark_as_done':
        if len(sys.argv) < 3:
            print("Please enter ID of task, which will be marked as done")
            sys.exit(1)
        try:
            id_ = int(sys.argv[2])
            if check_is_correct_id(id_) is False:
                print("No record with that ID")
                sys.exit(1)
        except ValueError:
            print("Please enter correct ID of task, which will be marked as done")
            sys.exit(1)
        else:
            mark_done(id_)
    elif command == 'list_not_done':
        list_not_done()
    elif command == 'delete_done':
        delete_done()
        print("Deleted done tasks")
    elif command == 'edit':
        if len(sys.argv) < 5:
            print("Please enter correct values to edit")
            sys.exit(1)

        try:
            id_ = int(sys.argv[2])
        except ValueError:
            print("Please enter correct ID of task, which will be edited")
            sys.exit(1)

        if check_is_correct_id(id_) is False:
            print("No record with that ID")
            sys.exit(1)

        if len(sys.argv[3].strip()) == 0:
            print("Please enter correct values which will be edited")
            sys.exit(1)
        if len(sys.argv[4].strip()) == 0:
            print("Please enter correct values which will be inserted")
            sys.exit(1)

        edit_task(id_, sys.argv[3], sys.argv[4])




