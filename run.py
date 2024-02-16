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
task_id = len(tasks)
# Define a separator for visual clarity in the log file
# separator= "-" * 100
separator = "-" * shutil.get_terminal_size().columns
# Define the filename for storing task logs
file_name = "tasks_log.txt"
desktop_path = Path.home() / "Desktop"
full_path = desktop_path / file_name


def parse_task_line(line):
    pass


def load_tasks():
    pass


def add_task_and_log(description):
    pass


def delete_task(idx):
    pass


def modify_task(task_id_to_modify):
    pass


def clear_screen():
    pass


def main():
    """
    The main function of the program. Handles user interaction.
    """
    init()
    if os.path.exists(full_path):
        load_tasks()
    print(Fore.GREEN + "Welcome to Developers' Task Manager")
    while True:
        time.sleep(2)
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
