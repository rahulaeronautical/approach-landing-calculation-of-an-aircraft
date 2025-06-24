import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D
import random
import csv
from datetime import datetime

# Core Calculations 
def calculate_approach(altitude, distance, time_min):
    angle_rad = math.atan(altitude / distance)
    angle_deg = math.degrees(angle_rad)
    distance_nm = distance / 6076.12
    speed_knots = distance_nm / (time_min / 60)
    return angle_deg, speed_knots

#Real-Time Sensor Simulation 
def get_real_time_data():
    altitude = random.uniform(1000, 2000)
    distance = random.uniform(10000, 15000)
    time_min = random.uniform(2.5, 4.0)
    return round(altitude, 2), round(distance, 2), round(time_min, 2)

#  CSV Logging 
def log_to_csv(altitude, distance, time_min, angle, speed):
    with open("approach_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), altitude, distance, time_min, f"{angle:.2f}", f"{speed:.2f}"])

# PDF Report Generation
def generate_pdf_report(altitude, distance, time_min, angle, speed):
    with PdfPages("approach_report.pdf") as pdf:
        fig, ax = plt.subplots()
        ax.plot([0, distance], [altitude, 0], marker='o')
        ax.set_title("Approach Path")
        ax.set_xlabel("Horizontal Distance (ft)")
        ax.set_ylabel("Altitude (ft)")
        ax.invert_yaxis()

        fig.text(0.1, 0.9, f"Approach Report", fontsize=14)
        fig.text(0.1, 0.85, f"Altitude: {altitude} ft")
        fig.text(0.1, 0.80, f"Distance: {distance} ft")
        fig.text(0.1, 0.75, f"Time: {time_min} min")
        fig.text(0.1, 0.70, f"Angle: {angle:.2f}°")
        fig.text(0.1, 0.65, f"Speed: {speed:.2f} knots")

        pdf.savefig(fig)
        plt.close()

# 3D Plotting 
def show_3d_path(altitude, distance):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot([0, distance], [0, 0], [altitude, 0], marker='o', color='red')
    ax.set_xlabel('Distance (ft)')
    ax.set_ylabel('Lateral Offset (ft)')
    ax.set_zlabel('Altitude (ft)')
    ax.set_title('3D Approach Path')
    plt.show()

#  Main Calculation + Plot 
def calculate_from_input():
    try:
        altitude = float(entry_altitude.get())
        distance = float(entry_distance.get())
        time_min = float(entry_time.get())

        angle, speed = calculate_approach(altitude, distance, time_min)

        label_result_angle.config(text=f"Approach Angle: {angle:.2f}°")
        label_result_speed.config(text=f"Speed: {speed:.2f} knots")

        # CSV Log + PDF + 2D Plot
        log_to_csv(altitude, distance, time_min, angle, speed)
        generate_pdf_report(altitude, distance, time_min, angle, speed)

        # 2D Plot
        plt.figure(figsize=(6, 4))
        plt.plot([0, distance], [altitude, 0], marker='o', color='blue')
        plt.title("Approach Path")
        plt.xlabel("Horizontal Distance (ft)")
        plt.ylabel("Altitude (ft)")
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.show()

        # Optional: 3D Path
        show_3d_path(altitude, distance)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def use_real_time_data():
    altitude, distance, time_min = get_real_time_data()
    entry_altitude.delete(0, tk.END)
    entry_distance.delete(0, tk.END)
    entry_time.delete(0, tk.END)
    entry_altitude.insert(0, altitude)
    entry_distance.insert(0, distance)
    entry_time.insert(0, time_min)
    calculate_from_input()

# GUI Setup 
root = tk.Tk()
root.title("Aircraft Approach Angle & Speed Analyzer")

# Labels and Entries
tk.Label(root, text="Altitude Loss (ft):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Label(root, text="Horizontal Distance (ft):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Label(root, text="Time Taken (min):").grid(row=2, column=0, padx=10, pady=5, sticky="e")

entry_altitude = tk.Entry(root)
entry_distance = tk.Entry(root)
entry_time = tk.Entry(root)

entry_altitude.grid(row=0, column=1, padx=10, pady=5)
entry_distance.grid(row=1, column=1, padx=10, pady=5)
entry_time.grid(row=2, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Calculate", command=calculate_from_input).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Use Real-Time Data", command=use_real_time_data).grid(row=4, column=0, columnspan=2, pady=5)

# Output Labels
label_result_angle = tk.Label(root, text="Approach Angle: --")
label_result_angle.grid(row=5, column=0, columnspan=2)

label_result_speed = tk.Label(root, text="Speed: --")
label_result_speed.grid(row=6, column=0, columnspan=2)

root.mainloop()
