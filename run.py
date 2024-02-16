"""
This module provides functionality for managing tasks for developers. It allows
users to add, modify, delete, and list tasks. Each task includes an ID, date,
time, and description. Tasks are stored in a log file on the user's desktop,
providing easy access and persistent storage.
"""

import os
import shutil
import time
from pathlib import Path

from colorama import init, Fore


# Initialize an empty list to store tasks
tasks = []
# Initialize task ID based on the current length of tasks
TASK_ID = len(tasks)
# Define a separator for visual clarity in the log file
# separator= "-" * 100
separator = "-" * shutil.get_terminal_size().columns
# Define the filename for storing task logs
# file_name = "tasks_log.txt"
#Unlock next two line to put your file on Desktop 
# desktop_path = Path.home() / "Desktop"
# full_path = desktop_path / file_name
LOG_FILE_NAME = os.getenv('TASKS_LOG_PATH', 'tasks_log.txt')

# Check if the LOG_FILE_NAME is an absolute path, if not, use the desktop path
if os.path.isabs(LOG_FILE_NAME):
    full_path = LOG_FILE_NAME
else:
    # If running locally, store the tasks log on the desktop for easy access
    desktop_path = Path.home() / "Desktop"
    full_path = desktop_path / LOG_FILE_NAME


def parse_task_line(line):
    """
    Parses a single line from the task log into a dictionary.

    Parameters:
    - line (str): A line from the task log file.

    Returns:
    - dict: A dictionary containing the parsed key-value pair if the line is valid.
    - None: If the line does not contain a colon (:) indicating a key-value pair.
    """
    if ":" not in line:
        return None
    key, value = line.split(":", 1)
    return {key.strip(): value.strip()}


def load_tasks():
    """
    Loads tasks from the log file into the global tasks list.
    """
    tasks = []
    task_group = []

    with open(full_path, "r+", encoding="utf-8") as file:
        for line in file:
            if line.strip() == "" or line.strip().startswith(separator):
                if task_group:
                    tasks.append(task_group)
                    task_group = []
            else:
                task_info = parse_task_line(line.strip())
                if task_info:
                    task_group.append(task_info)
        if task_group:
            tasks.append(task_group)


def add_task_and_log(description):
    """
    Adds a new task with the given description to the tasks list and logs it to the file.

    Parameters:
    - description (str): The description of the task to be added.
    """
    global TASK_ID
    TASK_ID = len(tasks) + 1

    now = time.time()
    timestamp = time.strftime("Date: %Y-%m-%d\nTime: %H:%M:%S", time.localtime(now))
    log_message = f"ID: {TASK_ID}\n{timestamp}\nTask: {description}\n{separator}\n"

    print(f"Task ID <{TASK_ID}>: <{description}> successfully added")
    tasks.append(
        {
            "ID": str(TASK_ID),
            "Date": time.strftime("%Y-%m-%d", time.localtime(now)),
            "Time": time.strftime("%H:%M:%S", time.localtime(now)),
            "Task": description,
        }
    )

    with open(full_path, "a+", encoding="utf-8") as file:
        file.seek(0)
        if not file.readlines():
            file.write(f"{'-'*74} List  Of Tasks: {'-'*74}\n")
        file.write(log_message)


def delete_task(idx):
    """
    Deletes a task based on its ID.

    Parameters:
    - idx (int): The ID of the task to be deleted.
    """
    global tasks
    idx = int(idx)

    tasks_to_keep = []
    found = False

    for task_group in tasks:
        for task_dict in task_group:
            if task_dict.get("ID") == str(idx):
                found = True
                break
        if not found:
            tasks_to_keep.append(task_group)
        found = False

    tasks = tasks_to_keep

    with open(full_path, "w+", encoding="utf-8") as file:
        lines = file.readlines()
        if not lines:
            file.write(f"{'-'*74} List Of Tasks: {'-'*74}\n")
        for task_group in tasks:
            for task_dict in task_group:
                for key, value in task_dict.items():
                    file.write(f"{key}: {value}\n")
            file.write(separator + "\n")

    if not found:
        print("Task ID not found.")


def modify_task(task_id_to_modify):
    """
    Modifies the description of a task based on its ID.

    Parameters:
    - task_id_to_modify (int): The ID of the task to modify.
    """
    global tasks
    load_tasks()
    found = False
    try:
        task_id_to_modify = int(task_id_to_modify)
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return

    for task_group in tasks:
        for task in task_group:
            if task.get("ID") == str(task_id_to_modify):
                new_description = input("Enter the new task description: ")
                for task_desc in task_group:
                    if "Task" in task_desc:
                        task_desc["Task"] = new_description
                        found = True
                        break
                if found:
                    break
        if found:
            break

    if found:
        print("Task successfully modified.")
        with open(full_path, "w+", encoding="utf-8") as file:
            lines = file.readlines()
            if not lines:
                file.write(f"{'-'*74} List Of Tasks: {'-'*74}\n")
            for task_group in tasks:
                for task in task_group:
                    for key, value in task.items():
                        file.write(f"{key}: {value}\n")
                file.write(separator + "\n")
    else:
        print("Task ID not found.")


def clear_screen():
    """
    Clears the console screen based on the operating system.
    """
    # Check if the operating system is Windows
    if os.name == "nt":
        os.system("cls")
    else:
        # Assume the operating system is Unix/Linux/Mac
        os.system("clear")


def main():
    """
    The main function of the program. Handles user interaction.
    """
    init()
    if os.path.exists(full_path):
        load_tasks()
    print(Fore.GREEN + "Welcome to Developers' Task Manager")
    while True:
        time.sleep(3)
        clear_screen()
        print("Developers Task Manager:\n")
        print("1: Add task\n2: Modify task\n3: Delete task\n4: Exit\n")
        choice = input("Select action: ")
        try:
            if choice == "1":
                add_task_and_log(input("Enter task: "))
            elif choice == "2":
                modify_task(input("Enter task to modify: "))
            elif choice == "3":
                delete_task(input("Choice task number: "))
            elif choice == "4":
                break
            else:
                print("Invalid selection. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
