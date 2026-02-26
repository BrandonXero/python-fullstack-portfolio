import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# ==============================
# DATA STORAGE
# ==============================

users = []
current_user = None

def load_users():
    global users
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
        if not isinstance(users, list):
            users = []
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

def save_users():
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# ==============================
# GUI FUNCTIONS
# ==============================

def refresh_profile_list():
    profile_listbox.delete(0, tk.END)
    for user in users:
        profile_listbox.insert(tk.END, user["username"])

def gui_create_profile():
    username = entry_profile_name.get()
    age = entry_profile_age.get()
    weight = entry_profile_weight.get()
    height = entry_profile_height.get()
    goal = entry_profile_goal.get()

    if not username:
        messagebox.showwarning("Input Error", "Please enter a name!")
        return

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
    refresh_profile_list()
    messagebox.showinfo("Success", f"Profile '{username}' created!")

def gui_select_profile():
    global current_user
    try:
        index = profile_listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a profile!")
        return

    current_user = users[index]
    messagebox.showinfo("Profile Selected", f"Current profile: {current_user['username']}")

def gui_add_workout():
    if current_user is None:
        messagebox.showwarning("Profile Error", "Select a profile first!")
        return

    exercise = entry_exercise.get()
    sets = entry_sets.get()
    reps = entry_reps.get()
    weight = entry_weight.get()
    notes = entry_notes.get()

    if not exercise:
        messagebox.showwarning("Input Error", "Enter an exercise name!")
        return

    workout = {
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "notes": notes,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    current_user["workouts"].append(workout)
    save_users()
    messagebox.showinfo("Workout Added", f"{exercise} added!")

def gui_view_workouts():
    if current_user is None:
        messagebox.showwarning("Profile Error", "Select a profile first!")
        return

    if not current_user["workouts"]:
        messagebox.showinfo("Workouts", "No workouts logged yet.")
        return

    workouts_text = ""
    for w in current_user["workouts"]:
        workouts_text += (
            f"{w['date']} - {w['exercise']}: "
            f"{w['sets']}x{w['reps']} @ {w['weight']} lbs"
        )
        if w["notes"]:
            workouts_text += f" | Notes: {w['notes']}"
        workouts_text += "\n"

    messagebox.showinfo(f"{current_user['username']}'s Workouts", workouts_text)

def gui_log_weight():
    if current_user is None:
        messagebox.showwarning("Profile Error", "Select a profile first!")
        return

    weight = entry_current_weight.get()
    if not weight:
        messagebox.showwarning("Input Error", "Enter a weight!")
        return

    entry_log = {
        "weight": weight,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    current_user["weight_logs"].append(entry_log)
    save_users()
    messagebox.showinfo("Weight Logged", f"{weight} lbs logged!")

def gui_view_weight_logs():
    if current_user is None:
        messagebox.showwarning("Profile Error", "Select a profile first!")
        return

    if not current_user["weight_logs"]:
        messagebox.showinfo("Weight Logs", "No weight logs yet.")
        return

    logs_text = ""
    for log in current_user["weight_logs"]:
        logs_text += f"{log['date']}: {log['weight']} lbs\n"

    messagebox.showinfo(f"{current_user['username']}'s Weight Logs", logs_text)

def gui_show_progress_chart():
    if current_user is None:
        messagebox.showwarning("Profile Error", "Select a profile first!")
        return

    if not current_user["weight_logs"]:
        messagebox.showinfo("Progress Chart", "No weight logs to display.")
        return

    dates = [log["date"] for log in current_user["weight_logs"]]
    weights = [float(log["weight"]) for log in current_user["weight_logs"]]

    plt.figure(figsize=(8,4))
    plt.plot(dates, weights, marker='o')
    plt.title(f"Weight Progress for {current_user['username']}")
    plt.xlabel("Date")
    plt.ylabel("Weight (lbs)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ==============================
# GUI LAYOUT
# ==============================

load_users()

root = tk.Tk()
root.title("Fitness Tracker")
root.geometry("650x650")

# -------- Profiles --------
frame_profiles = tk.LabelFrame(root, text="Profiles", padx=10, pady=10)
frame_profiles.pack(fill="x", padx=10, pady=5)

tk.Label(frame_profiles, text="Name:").grid(row=0, column=0)
entry_profile_name = tk.Entry(frame_profiles)
entry_profile_name.grid(row=0, column=1)

tk.Label(frame_profiles, text="Age:").grid(row=1, column=0)
entry_profile_age = tk.Entry(frame_profiles)
entry_profile_age.grid(row=1, column=1)

tk.Label(frame_profiles, text="Weight:").grid(row=2, column=0)
entry_profile_weight = tk.Entry(frame_profiles)
entry_profile_weight.grid(row=2, column=1)

tk.Label(frame_profiles, text="Height:").grid(row=3, column=0)
entry_profile_height = tk.Entry(frame_profiles)
entry_profile_height.grid(row=3, column=1)

tk.Label(frame_profiles, text="Goal:").grid(row=4, column=0)
entry_profile_goal = tk.Entry(frame_profiles)
entry_profile_goal.grid(row=4, column=1)

tk.Button(frame_profiles, text="Create Profile", command=gui_create_profile).grid(row=5, column=0, pady=5)
tk.Button(frame_profiles, text="Select Profile", command=gui_select_profile).grid(row=5, column=1, pady=5)

profile_listbox = tk.Listbox(frame_profiles, height=4)
profile_listbox.grid(row=6, column=0, columnspan=2, pady=5)

refresh_profile_list()

# -------- Workouts --------
frame_workout = tk.LabelFrame(root, text="Workouts", padx=10, pady=10)
frame_workout.pack(fill="x", padx=10, pady=5)

tk.Label(frame_workout, text="Exercise:").grid(row=0, column=0)
entry_exercise = tk.Entry(frame_workout)
entry_exercise.grid(row=0, column=1)

tk.Label(frame_workout, text="Sets:").grid(row=1, column=0)
entry_sets = tk.Entry(frame_workout)
entry_sets.grid(row=1, column=1)

tk.Label(frame_workout, text="Reps:").grid(row=2, column=0)
entry_reps = tk.Entry(frame_workout)
entry_reps.grid(row=2, column=1)

tk.Label(frame_workout, text="Weight:").grid(row=3, column=0)
entry_weight = tk.Entry(frame_workout)
entry_weight.grid(row=3, column=1)

tk.Label(frame_workout, text="Notes:").grid(row=4, column=0)
entry_notes = tk.Entry(frame_workout)
entry_notes.grid(row=4, column=1)

tk.Button(frame_workout, text="Add Workout", command=gui_add_workout).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(frame_workout, text="View Workouts", command=gui_view_workouts).grid(row=6, column=0, columnspan=2, pady=5)

# -------- Weight Logs --------
frame_weight = tk.LabelFrame(root, text="Weight Logs", padx=10, pady=10)
frame_weight.pack(fill="x", padx=10, pady=5)

tk.Label(frame_weight, text="Current Weight:").grid(row=0, column=0)
entry_current_weight = tk.Entry(frame_weight)
entry_current_weight.grid(row=0, column=1)

tk.Button(frame_weight, text="Log Weight", command=gui_log_weight).grid(row=1, column=0, pady=5)
tk.Button(frame_weight, text="View Weight Logs", command=gui_view_weight_logs).grid(row=1, column=1, pady=5)
tk.Button(frame_weight, text="Show Progress Chart", command=gui_show_progress_chart).grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()
