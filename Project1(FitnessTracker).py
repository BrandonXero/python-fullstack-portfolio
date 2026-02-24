import json #used for saving and loading data

# This list will hold all user data
users = []
current_user = None # This stores the selected user
#
#LOAD USERS FROM FILE
#

def load_users():
    global users 
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
        if not isinstance(users, list):
            users = []
    except (FileNotFoundError, json.JSONDecodeError):
        users = []    

#
# SAVE USERS TO FILE
#

def save_users():
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

#
# CREATE NEW PROFILE
#

def create_profile():
    username = input("Enter Your preferred name: ")
    age = input("Enter your age: ")
    weight = input("Enter your weight (lbs): ")
    height = input("Enter your height (inches): ")
    goal = input("Enter your fitness goal: ")

    user = {
        "username": username,
        "age": age,
        "weight": weight,
        "height": height,
        "goal": goal,
        "workouts": [],
        "weight_logs": []
    }

    users.append(user)
    save_users()
    print(f"\nprofile for {username} created successfully!")

#
#SELECT EXISTING PROFILE
#

def select_profile():
    global current_user
    if len(users) == 0:
        print("\nNo profiles are available. Please create a profile.")
        return
    
    print("\nAvailable profiles:")
    for i, user in enumerate(users):
        print(f"{i + 1}. {user['username']}")

    try:
      choice = int(input("Select a profile number: ")) - 1
      if 0 <= choice < len(users):
        current_user = users[choice]
        print(f"\nProfile {current_user['username']} selected!")
      else:
        print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")

from datetime import datetime # To add data automantically

#
# ADD WORKOUT
#

def add_workout():
    global current_user
    if current_user is None:
        print("\nPlease select a profile first!")
        return

    # Ask for workout info
    exercise = input("Enter exercise name: ")
    sets = input("Enter number of sets: ")
    reps = input("Enter number of reps: ")
    weight = input("Enter weight used (lbs): ")
    notes = input("Add any notes (optional): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Create workout object
    workout = {
        "exercise": exercise,
        "sets": sets, 
        "reps": reps,
        "weight": weight,
        "notes": notes,
        "date": date
    }

    # Add to current user and save
    current_user["workouts"].append(workout)
    save_users()
    print(f"\nWorkout for {exercise} added successfully!")

#
# VIEW WORKOUTS
#

def view_workouts():
    # 1️ Check if a profile is selected
    if current_user is None:
        print("\nPlease select a profile first!")
        return

    # 2️ Check if any workouts exist
    if len(current_user["workouts"]) == 0:
        print("\nNo workouts have been logged yet.")
        return

    # 3️ Print all workouts
    print(f"\n--- Workouts for {current_user['username']} ---")
    for i, workout in enumerate(current_user["workouts"]):
        print(f"{i+1}. {workout['date']} - {workout['exercise']}: "
              f"{workout['sets']} sets x {workout['reps']} reps @ {workout['weight']} lbs")
        if workout['notes']:
            print(f" Notes: {workout['notes']}")

#
#   MAIN MENU
#

def show_menu():
    print("\n--- Fitness Tracker ---")
    print("1. Create profile")
    print("2. Select Profile")
    print("3. Add Workout")
    print("4. View Workouts")
    print("5. Exit")

#
# RUN PROGRAM
#

load_users()

while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        create_profile()
    elif choice == "2":
        select_profile()
    elif choice == "3":
        add_workout()
    elif choice == "4":
        view_workouts()
    elif choice == "5":
        break
    else:
        print("Invalid option. Try again.")