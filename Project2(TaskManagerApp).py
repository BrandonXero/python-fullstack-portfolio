import json
import os

# Global Task list
tasks = []

# -------------------------
# Load tasks from file
# -------------------------
def load_tasks():
    global tasks
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)

            # Ensure tasks is a list of dictionaries
            if not isinstance(tasks, list):
                tasks = []
            else:
                tasks = [t for t in tasks if isinstance(t, dict)]

        except (json.JSONDecodeError, ValueError):
            tasks = []
    else:
        tasks = []

# -------------------------
# Save tasks to file
# -------------------------
def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

# -------------------------
# Add Task
# -------------------------
def add_task():
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    priority = input("Enter priority (Low/Medium/High): ").strip().capitalize()
    if priority not in ["Low", "Medium", "High"]:
        print("Invalid priority. Please use Low, Medium, or High.")
        return

    task = {
        "title": title,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    save_tasks()
    print("Task added successfully!")

# -------------------------
# View Tasks
# -------------------------
def view_tasks():
    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks):
        status = "✓" if task.get("completed") else "✗"
        print(f"{i + 1}. [{status}] {task.get('title', 'Untitled')} ({task.get('priority', 'Unknown')})")

# -------------------------
# Mark Task Complete
# -------------------------
def complete_task():
    view_tasks()
    if not tasks:
        return

    try:
        choice = int(input("Enter task number to mark complete: "))
        if choice < 1 or choice > len(tasks):
            print("Invalid selection.")
            return

        tasks[choice - 1]["completed"] = True
        save_tasks()
        print("Task marked as complete!")
    except ValueError:
        print("Please enter a number.")

# -------------------------
# Delete Task
# -------------------------
def delete_task():
    view_tasks()
    if not tasks:
        return

    try:
        choice = int(input("Enter task number to delete: "))
        if choice < 1 or choice > len(tasks):
            print("Invalid selection.")
            return

        tasks.pop(choice - 1)
        save_tasks()
        print("Task deleted!")
    except ValueError:
        print("Please enter a number.")

# -------------------------
# View Incomplete Tasks
# -------------------------
def view_incomplete_tasks():
    incomplete = [t for t in tasks if not t.get("completed")]

    if not incomplete:
        print("No incomplete tasks 🎉")
        return

    for i, task in enumerate(incomplete):
        print(f"{i + 1}. [✗] {task.get('title', 'Untitled')} ({task.get('priority', 'Unknown')})")

# -------------------------
# Sort Tasks by Priority
# -------------------------
def sort_tasks_by_priority():
    priority_rank = {"High": 1, "Medium": 2, "Low": 3}

    tasks.sort(key=lambda t: priority_rank.get(t.get("priority", ""), 99))
    save_tasks()
    print("Tasks sorted by priority (High → Low).")

# -------------------------
# Main Menu
# -------------------------
def main():
    load_tasks()

    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. View Incomplete Tasks")
        print("6. Sort by Priority")
        print("7. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            view_incomplete_tasks()
        elif choice == "6":
            sort_tasks_by_priority()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()